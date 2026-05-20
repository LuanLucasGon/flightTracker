# ✈️ Flight Tracker

Rastreador de voos pessoal em tempo real. Informe o número da sua passagem e acompanhe o avião se movendo no mapa, com a rota sendo desenhada em tempo real, informações dos aeroportos de origem e destino, e notificações de eventos do voo.

> Projeto de estudo — sem fins comerciais.

---

## 📸 Visão do produto

- Mapa interativo com o ícone do avião rotacionando de acordo com o heading real
- Rota real desenhada ponto a ponto conforme o avião se move
- Rota planejada (origem → destino) traçada ao cadastrar a passagem
- Marcadores dos aeroportos de origem e destino com informações
- Notificações em tempo real: decolagem, pouso, atraso, atualização de rota
- Feed de notificações pessoal por passagem

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────┐
│                   PostgreSQL                         │
│                                                      │
│  usuarios   passagens   aeroportos   posicoes        │
│                         (OurAirports  historico      │
│                          importado)   do voo         │
└─────────────────────────────────────────────────────┘
         ↑                              ↑
         │                              │ salva
┌────────────────┐           ┌─────────────────────┐
│   Flask API    │           │  Polling Scheduler  │
│                │           │  (a cada 10s por    │
│  /usuarios     │           │   voo ativo hoje)   │
│  /passagens    │           └─────────┬───────────┘
│  /aeroportos   │                     │ publica
│  /voos         │           ┌─────────▼───────────┐
└────────┬───────┘           │      RabbitMQ        │
         │ WebSocket         │                      │
         │              ┌────▼──────┐  ┌──────────┐ │
         │              │ Consumer  │  │ Consumer │ │
         │              │ Posição   │  │ Eventos  │ │
         │              │ → salva   │  │ → notif  │ │
         │              │ → WS emit │  └──────────┘ │
         │              └─────┬─────┘  └────────────┘
         │                    │ emite
┌────────▼────────────────────▼───────┐
│            Angular Frontend          │
│                                      │
│  ┌─────────────────────────────┐    │
│  │        Leaflet Map          │    │
│  │  • ícone avião (rotaciona)  │    │
│  │  • rota real (polyline)     │    │
│  │  • rota planejada (dashed)  │    │
│  │  • marcadores aeroportos    │    │
│  │  • info card do voo         │    │
│  └─────────────────────────────┘    │
│                                      │
│  ┌──────────┐  ┌────────────────┐   │
│  │ Painel   │  │ Notificações   │   │
│  │ do voo   │  │ (toast/feed)   │   │
│  └──────────┘  └────────────────┘   │
└──────────────────────────────────────┘
```

---

## 🛠️ Stack

| Camada | Tecnologia | Versão | Motivo |
|---|---|---|---|
| Backend | Python + Flask | 3.12+ / 3.1 | API REST + WebSocket |
| ORM | SQLAlchemy + Flask-Migrate | 3.1 / 4.0 | Migrations versionadas |
| Banco de dados | PostgreSQL | 16 | Relacional, suporte a UUID e índices geoespaciais |
| Mensageria | RabbitMQ | 3.13 | Desacopla polling de entrega de notificações |
| Tempo real | Flask-SocketIO | 5.3 | WebSocket para mover o avião no mapa |
| Autenticação | JWT (flask-jwt-extended) | 4.6 | Stateless, compatível com mobile |
| Testes | pytest + pytest-mock | latest | TDD — teste antes do código |
| Frontend web | Angular | 17 | SPA componentizada |
| Mapa | Leaflet.js | 1.9 | Leve, gratuito, ícone rotacionável |
| Tiles | Carto Dark Matter | — | Visual escuro ideal para rastreamento |
| App mobile | Flutter | 3.x | iOS + Android com código único |
| Containers | Docker + Docker Compose | 29 / v5 | Ambiente reproduzível |
| API de voos | OpenSky Network | — | Gratuita, posição ADS-B em tempo real |
| Base aeroportos | OurAirports CSV | — | Dataset público, importado localmente |

---

## 📁 Estrutura do projeto

```
flight-tracker/
│
├── backend/                          # API Flask
│   ├── app/
│   │   ├── usuarios/                 # Domínio: autenticação
│   │   │   ├── usuario_entity.py     # Model SQLAlchemy
│   │   │   ├── usuario_dto.py        # Request/Response DTOs
│   │   │   ├── usuario_repository.py # Acesso ao banco
│   │   │   ├── usuario_service.py    # Regras de negócio
│   │   │   └── usuario_controller.py # Blueprint Flask (HTTP only)
│   │   │
│   │   ├── passagens/                # Domínio: passagens aéreas
│   │   │   ├── passagem_entity.py
│   │   │   ├── passagem_dto.py
│   │   │   ├── passagem_repository.py
│   │   │   ├── passagem_service.py
│   │   │   └── passagem_controller.py
│   │   │
│   │   ├── aeroportos/               # Domínio: aeroportos (OurAirports)
│   │   │   ├── aeroporto_entity.py
│   │   │   ├── aeroporto_dto.py
│   │   │   ├── aeroporto_repository.py
│   │   │   ├── aeroporto_service.py
│   │   │   └── aeroporto_controller.py
│   │   │
│   │   ├── voos/                     # Domínio: rastreamento em tempo real
│   │   │   ├── posicao_entity.py     # Snapshot de posição GPS
│   │   │   ├── posicao_dto.py
│   │   │   ├── posicao_repository.py
│   │   │   ├── opensky_client.py     # Client da API OpenSky
│   │   │   ├── voo_service.py        # Polling + publicação RabbitMQ
│   │   │   └── voo_controller.py
│   │   │
│   │   ├── notificacoes/             # Domínio: notificações
│   │   │   ├── notificacao_entity.py
│   │   │   ├── notificacao_dto.py
│   │   │   ├── notificacao_repository.py
│   │   │   ├── notificacao_service.py
│   │   │   └── notificacao_controller.py
│   │   │
│   │   ├── workers/                  # Consumers RabbitMQ
│   │   │   ├── posicao_consumer.py   # Salva posição + emite WebSocket
│   │   │   └── evento_consumer.py    # Processa eventos → notificações
│   │   │
│   │   └── shared/                   # Infraestrutura transversal
│   │       ├── database/
│   │       │   └── extensions.py     # db, migrate, jwt, socketio
│   │       ├── messaging/
│   │       │   └── rabbitmq_client.py # Publish/consume RabbitMQ
│   │       ├── exceptions/
│   │       │   └── domain_exceptions.py
│   │       └── middlewares/
│   │           └── error_handler.py
│   │
│   ├── tests/                        # Testes (TDD)
│   │   ├── usuarios/
│   │   │   ├── test_usuario_service.py
│   │   │   └── test_usuario_controller.py
│   │   ├── passagens/
│   │   │   ├── test_passagem_service.py
│   │   │   └── test_passagem_controller.py
│   │   ├── voos/
│   │   │   ├── test_opensky_client.py
│   │   │   └── test_voo_service.py
│   │   ├── notificacoes/
│   │   │   └── test_notificacao_service.py
│   │   └── conftest.py               # Fixtures compartilhadas
│   │
│   ├── migrations/                   # Flask-Migrate (Alembic)
│   ├── run.py                        # Entrypoint API
│   ├── worker.py                     # Entrypoint consumers RabbitMQ
│   ├── requirements.txt
│   ├── requirements-dev.txt          # pytest, pytest-mock, faker
│   ├── Dockerfile
│   ├── Dockerfile.worker
│   └── .env.example
│
├── frontend/                         # Angular 17
│   └── src/
│       └── app/
│           ├── usuarios/             # Feature: auth
│           │   ├── usuario.model.ts
│           │   ├── usuario.service.ts
│           │   ├── login/            # Componente de login
│           │   └── registro/         # Componente de registro
│           │
│           ├── passagens/            # Feature: passagens
│           │   ├── passagem.model.ts
│           │   ├── passagem.service.ts
│           │   ├── lista/            # Componente lista de passagens
│           │   └── formulario/       # Componente cadastro
│           │
│           ├── mapa/                 # Feature: mapa em tempo real
│           │   ├── mapa.model.ts
│           │   ├── mapa.service.ts   # Leaflet + WebSocket
│           │   ├── mapa-container/   # Componente container do mapa
│           │   ├── aviao-icon/       # Componente ícone rotacionável
│           │   ├── rota-real/        # Componente polyline da rota
│           │   ├── rota-planejada/   # Componente linha origem→destino
│           │   └── aeroporto-marker/ # Componente marcador de aeroporto
│           │
│           ├── notificacoes/         # Feature: notificações
│           │   ├── notificacao.model.ts
│           │   ├── notificacao.service.ts
│           │   ├── feed/             # Componente feed de notificações
│           │   └── toast/            # Componente toast em tempo real
│           │
│           └── shared/               # Infraestrutura Angular
│               ├── interceptors/
│               │   └── auth.interceptor.ts
│               ├── guards/
│               │   └── auth.guard.ts
│               └── components/
│                   └── loading/      # Componente de loading
│
├── mobile/                           # Flutter 3
│   └── lib/
│       ├── usuarios/
│       ├── passagens/
│       ├── voos/
│       ├── notificacoes/
│       └── shared/
│           └── api_client.dart
│
├── infra/
│   ├── init.sql                      # Schema inicial do banco
│   └── dados/
│       └── airports.csv              # OurAirports (baixar manualmente)
│
├── docker-compose.yml                # PostgreSQL + RabbitMQ
├── docker-compose.dev.yml            # Overrides para desenvolvimento
└── README.md
```

---

## 🚀 Como rodar

### Pré-requisitos

- Docker Desktop 29+ rodando
- Python 3.12+
- Node.js 20+
- Flutter 3.x (para o mobile)

### 1. Clonar e configurar variáveis de ambiente

```bash
git clone https://github.com/seu-usuario/flight-tracker.git
cd flight-tracker
cp backend/.env.example backend/.env
```

Edite `backend/.env` com suas configurações.

### 2. Subir a infraestrutura (banco + mensageria)

```bash
docker compose up -d
```

Isso sobe:
- **PostgreSQL 16** na porta `5432`
- **RabbitMQ 3.13** na porta `5672` (management UI em `15672`)

Aguarde os containers ficarem healthy:

```bash
docker compose ps
```

### 3. Rodar o backend

```bash
cd backend
pip install -r requirements.txt -r requirements-dev.txt
flask db upgrade
python run.py
```

API disponível em `http://localhost:5000`

### 4. Rodar o consumer RabbitMQ (terminal separado)

```bash
cd backend
python worker.py
```

### 5. Importar base de aeroportos

```bash
# Baixar o CSV em: https://ourairports.com/data/airports.csv
# Salvar em infra/dados/airports.csv
cd backend
python -m app.aeroportos.importar_aeroportos
```

### 6. Rodar o frontend

```bash
cd frontend
npm install
npm start
```

Frontend em `http://localhost:4200`

### 7. Rodar o app mobile

```bash
cd mobile
flutter pub get
flutter run
```

---

## 🧪 Testes

O projeto segue **TDD estrito** — nenhum código de produção é escrito sem um teste falhando primeiro.

```bash
cd backend

# Rodar todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=term-missing

# Apenas um domínio
pytest tests/usuarios/ -v

# Watch mode (reexecuta ao salvar)
pytest-watch
```

### Filosofia de testes

- **Testes de service**: validam regras de negócio com mocks de repository
- **Testes de controller**: validam contratos HTTP (status codes, payloads, erros)
- **Testes de integração**: validam fluxos completos com banco real (pytest-docker ou banco de teste)
- **Nenhum teste trivial**: não testamos se `1 + 1 == 2`, testamos se um usuário com email duplicado recebe `409`, se um voo ativo hoje é incluído no polling, se um evento de decolagem gera a notificação correta

---

## 🔌 API REST

### Autenticação

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/usuarios/registrar` | Cria conta |
| `POST` | `/api/usuarios/login` | Login → retorna JWT |

### Passagens

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/passagens/` | Lista passagens do usuário |
| `POST` | `/api/passagens/` | Cadastra nova passagem |
| `GET` | `/api/passagens/:id` | Detalha passagem |
| `DELETE` | `/api/passagens/:id` | Remove passagem |

### Voos

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/voos/:passagem_id/posicao` | Posição atual |
| `GET` | `/api/voos/:passagem_id/historico` | Histórico de posições (rota real) |

### Aeroportos

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/aeroportos/buscar?q=GRU` | Busca aeroporto por código IATA/ICAO ou nome |

### Notificações

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/notificacoes/` | Lista notificações do usuário |
| `PATCH` | `/api/notificacoes/:id/lida` | Marca como lida |
| `GET` | `/api/notificacoes/nao-lidas/count` | Contador de não lidas |

---

## 📡 WebSocket

Após conectar, o cliente entra na sala do seu usuário:

```json
// Cliente emite
{ "event": "entrar_sala", "data": { "usuario_id": "uuid" } }

// Servidor emite — atualização de posição (~10s)
{ "event": "posicao_atualizada", "data": {
    "passagem_id": "uuid",
    "callsign": "GLO1234",
    "latitude": -23.4356,
    "longitude": -46.4731,
    "altitude_m": 10972,
    "velocidade_kmh": 891,
    "heading": 127.4,
    "no_solo": false,
    "capturado_em": "2024-03-15T14:32:10Z"
}}

// Servidor emite — evento de estado
{ "event": "notificacao", "data": {
    "tipo": "decolagem",
    "titulo": "✈️ Decolagem detectada",
    "mensagem": "GLO1234 decolou de GRU"
}}
```

---

## 🗺️ Fontes de dados

### OpenSky Network
- **URL**: https://opensky-network.org
- **Custo**: Gratuito
- **Limite**: 400 req/dia sem conta · 4.000 créditos/dia com conta gratuita
- **Dados**: Posição ADS-B em tempo real (lat, lng, altitude, velocidade, heading)

### OurAirports
- **URL**: https://ourairports.com/data/
- **Custo**: Gratuito, domínio público
- **Arquivo**: `airports.csv` (~60MB, ~80.000 aeroportos)
- **Dados**: Código IATA/ICAO, nome, cidade, país, coordenadas

---

## 🗺️ Visualização do mapa

| Elemento | Implementação |
|---|---|
| Mapa base | Leaflet.js 1.9 |
| Tiles | Carto Dark Matter (gratuito, sem chave) |
| Ícone do avião | SVG rotacionado via CSS `transform: rotate({heading}deg)` |
| Rota real | `L.Polyline` alimentada pelo histórico de posições |
| Rota planejada | `L.Polyline` tracejada entre coordenadas dos aeroportos |
| Marcadores | `L.Marker` customizado para aeroportos de origem e destino |

---

## 📋 Roadmap de implementação

### Fase 1 — Fundação
- [x] Arquitetura definida
- [ ] Docker Compose (PostgreSQL + RabbitMQ)
- [ ] Estrutura de pastas e configuração do projeto
- [ ] Cadastro e autenticação de usuário (TDD)

### Fase 2 — Core do produto
- [ ] Cadastro de passagem + lookup de aeroporto
- [ ] Importação da base OurAirports
- [ ] Polling OpenSky + publicação RabbitMQ
- [ ] Consumer de posição + emissão WebSocket

### Fase 3 — Visualização
- [ ] Mapa Leaflet no Angular
- [ ] Ícone do avião rotacionando em tempo real
- [ ] Rota real (polyline dos pontos capturados)
- [ ] Rota planejada (origem → destino tracejado)
- [ ] Marcadores e info cards dos aeroportos

### Fase 4 — Notificações
- [ ] Consumer de eventos (decolagem, pouso, atraso)
- [ ] Feed de notificações no frontend
- [ ] Toast em tempo real no mapa

### Fase 5 — Mobile
- [ ] App Flutter com mapa e notificações

---

## 📐 Princípios aplicados

**SOLID**
- **S** — cada classe tem uma única responsabilidade (repository só acessa banco, service só aplica regras)
- **O** — consumers RabbitMQ abertos para extensão (novo canal de notificação = novo consumer)
- **L** — DTOs e entities substituíveis sem quebrar contratos
- **I** — interfaces de repository segregadas por domínio
- **D** — services dependem de abstrações, não de implementações concretas

**Clean Code**
- Nomes que revelam intenção
- Funções com responsabilidade única
- Zero comentários explicando código ruim — o código deve se explicar
- Sem duplicação — DRY aplicado em BE e FE

**Performance**
- Zero N+1 — queries auditadas, joins explícitos onde necessário
- Polling desacoplado da entrega via RabbitMQ
- Histórico de posições indexado por `callsign` e `capturado_em`
- WebSocket apenas para dados em tempo real — REST para o resto

---

## 👨‍💻 Desenvolvimento

Este projeto é construído em modo **TDD estrito**:

1. Escreve o teste (Red 🔴)
2. Escreve o mínimo de código para passar (Green 🟢)
3. Refatora mantendo os testes verdes (Refactor 🔵)

Nenhum código de produção existe sem um teste cobrindo sua regra de negócio.

---

## 📄 Licença

MIT — uso livre para fins educacionais.