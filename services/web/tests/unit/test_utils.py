import pytest
from pydantic import ValidationError

from services.web.flask_app.registration.utils import CreateUserService
from services.web.flask_app.validators import RegistrationForm


def test_create_valid_user(client):
    form = RegistrationForm(username="kupriyanov", password="strongpwd", email="kupriyanovart@gmail.com")
    service = CreateUserService(form)
    user = service.create_user_for_registration()
    assert not service.already_exist()
    assert user.password_hash
    assert not user.confirmed


def test_user_already_exists(client):
    form = RegistrationForm(username="artem", email="123@gmail.com", password="123pwd")
    service = CreateUserService(form)
    assert service.already_exist()


def test_invalid_username(client):
    with pytest.raises(ValidationError):
        form = RegistrationForm(username="kupriyanov" * 50, password="strongpwd", email="hello@gmail.com")


def test_invalid_password(client):
    with pytest.raises(ValidationError):
        form = RegistrationForm(username="kupriyanov", password="strongpwd" * 120, email="hello@gmail.com")


def test_invalid_email(client):
    with pytest.raises(ValidationError):
        form = RegistrationForm(username="kupriyanov", password="strongpwd", email="hello.gmail.com")
