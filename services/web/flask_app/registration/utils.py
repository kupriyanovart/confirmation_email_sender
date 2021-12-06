import json

from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import or_

from .rmq_setting import RabbitMQMailPublisher
from ..models import User, db
from ..validators import RegistrationForm


class CreateTokenService:
    def __init__(self, serializer=None):
        self.serializer = serializer or URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    def get_token(self, data):
        return self.serializer.dumps(data)

    def get_email(self, token):
        return self.serializer.loads(token)


class CreateUserService:
    def __init__(self, form: RegistrationForm):
        self.form = form

    def already_exist(self):
        return db.session.query(User).filter(
            or_(User.username == self.form.username, User.email == self.form.email)
        ).one_or_none()

    def create_user_for_registration(self) -> User:
        token = CreateTokenService().get_token(self.form.email)
        user = User(username=self.form.username, email=self.form.email, token=token, confirmed=False)
        user.set_password(self.form.password)
        return user


class UserConfirmationService:
    def __init__(self, user, publisher=RabbitMQMailPublisher):
        self.user = user
        self.email_publisher = publisher()

    def send_confirmation(self, **kwargs):
        body = json.dumps(kwargs)
        self.email_publisher.publish(body=body)


class ConfirmationService:
    def __init__(self, token):
        self.token = token

    def get_user(self) -> User:
        return db.session.query(User).filter(User.token == self.token).one()

    def get_email_from_token(self) -> str:
        return CreateTokenService().get_email(self.token)
        