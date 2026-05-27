import os
from flask import Flask
from flask_cors import CORS

from app.shared.database.extensions import db, migrate, jwt, socketio
from app.shared.middlewares.error_handler import register_error_handlers


def create_app() -> Flask:
    app = Flask(__name__)
    _configure(app)
    _initialize_extensions(app)
    _register_blueprints(app)
    _import_models()
    register_error_handlers(app)

    @app.get("/api/health")
    def health():
        return {"status": "ok", "version": "1.0.0"}

    return app


def _configure(app: Flask) -> None:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = __import__("datetime").timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 24))
    )


def _initialize_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    socketio.init_app(app)


def _register_blueprints(app: Flask) -> None:
    from app.users.user_controller import users_bp
    from app.tickets.ticket_controller import tickets_bp
    from app.airports.airport_controller import airports_bp
    from app.flights.flight_controller import flights_bp
    from app.notifications.notification_controller import notifications_bp

    app.register_blueprint(users_bp,         url_prefix="/api/users")
    app.register_blueprint(tickets_bp,        url_prefix="/api/tickets")
    app.register_blueprint(airports_bp,       url_prefix="/api/airports")
    app.register_blueprint(flights_bp,        url_prefix="/api/flights")
    app.register_blueprint(notifications_bp,  url_prefix="/api/notifications")


def _import_models() -> None:
    from app.users.user_entity import User                        # noqa: F401
    from app.tickets.ticket_entity import Ticket                  # noqa: F401
    from app.airports.airport_entity import Airport               # noqa: F401
    from app.flights.position_entity import Position              # noqa: F401
    from app.notifications.notification_entity import Notification # noqa: F401