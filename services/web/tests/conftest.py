# run tests -> $python -m pytest
import pytest

from services.web.flask_app import create_app, config
from services.web.flask_app.models import db, User


@pytest.fixture
def app():
    app = create_app(config.TestingConfig)
    app.app_context().push()
    create_table()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def create_table():
    user = User(username="artem", email="123@gmail.com", token="123token123", password_hash="123strong")
    db.drop_all()
    db.create_all()
    db.session.add(user)
    db.session.commit()
