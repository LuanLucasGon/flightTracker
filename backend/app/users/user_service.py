import secrets
from datetime import datetime, timedelta, timezone

from app.shared.email.templates.confirmation_email import build_confirmation_email
from app.shared.exceptions.domain_exceptions import ConflictException, InvalidDataException
from app.shared.messaging.rabbitmq_client import RabbitMQClient
from app.shared.validators.cpf_validator import is_valid_cpf
from app.users.user_repository import UserRepository


class UserService:
    def __init__(self):
        self._repository = UserRepository()
        self._rabbitmq = RabbitMQClient()

    def register_step1(self, email: str, cpf: str, password: str) -> None:
        self._validate_step1(email, cpf, password)

        token = secrets.token_urlsafe(32)

        self._rabbitmq.publish(
            queue="email.confirmation",
            message={
                "to": email,
                "subject": "Confirme seu email — Flight Tracker",
                "html": build_confirmation_email(
                    name="",
                    confirmation_url=f"http://localhost:4200/confirm?token={token}",
                ),
            },
        )

    def _validate_step1(self, email: str, cpf: str, password: str) -> None:
        if self._repository.email_exists(email):
            raise ConflictException("email already registered")

        if self._repository.cpf_exists(cpf):
            raise ConflictException("cpf already registered")

        if not is_valid_cpf(cpf):
            raise InvalidDataException("invalid cpf")

        if len(password) < 8:
            raise InvalidDataException("password must be at least 8 characters")