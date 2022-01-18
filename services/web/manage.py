from flask.cli import FlaskGroup


from flask_app.models import db, User
from flask_app.app import app


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(
        User(username="artem", email="123@gmail.com", token="123token123", password_hash="123strong")
    )
    db.session.commit()


if __name__ == "__main__":
    cli()
