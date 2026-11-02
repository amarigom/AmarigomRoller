import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from extensions import db  # noqa: E402
from factory import create_app  # noqa: E402
from models import User  # noqa: E402
from services.users import UserService  # noqa: E402
from strategies.notifications import Notifier  # noqa: E402

PASSWORD = "clave-segura-123"


class FakeNotifier(Notifier):
    def __init__(self):
        self.sent = []

    def send(self, subject, html, to):
        self.sent.append((subject, html, to))


@pytest.fixture()
def app(tmp_path):
    app = create_app({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(tmp_path / "test.db"),
        "SECRET_KEY": "test-secret-test-secret-test-secret-123",
        "TESTING": True,
        "QUOTE_RECIPIENT": "taller@example.com",
        "LOGIN_MAX_ATTEMPTS": 3,
    })
    app.extensions["notifier"] = FakeNotifier()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def _crear_usuario(rol, email=None):
    from models import Role
    from schemas.auth import UserCreateIn
    return UserService().create_user(UserCreateIn(
        email=email or f"{rol}@example.com", nombre=rol.title(), password=PASSWORD, rol=Role(rol)))


def _login(client, email):
    r = client.post("/api/auth/login", json={"email": email, "password": PASSWORD})
    assert r.status_code == 200, r.get_json()
    return {"Authorization": "Bearer " + r.get_json()["token"]}


@pytest.fixture()
def auth(client):
    """Devuelve headers de autenticaciÃ³n para el rol pedido: auth('admin')."""
    def _auth(rol):
        if not User.query.filter_by(email=f"{rol}@example.com").first():
            _crear_usuario(rol)
        return _login(client, f"{rol}@example.com")
    return _auth

