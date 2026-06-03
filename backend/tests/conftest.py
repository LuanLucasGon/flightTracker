import pytest
import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET_KEY"] = "test-secret"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["FLASK_ENV"] = "testing"
os.environ["RABBITMQ_URL"] = "amqp://guest:guest@localhost:5672/"

from app import create_app
from app.shared.database.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    test_app = create_app()
    test_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret",
        "SECRET_KEY": "test-secret",
    })

    with test_app.app_context():
        _db.create_all()
        yield test_app
        _db.drop_all()


@pytest.fixture(scope="function")
def db(app):
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()
        yield _db
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()