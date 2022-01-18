from flask import Flask
from flask_migrate import Migrate

from .config import Config
from . import models


migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    models.db.init_app(app)
    migrate.init_app(app, models.db)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .registration import bp as registration_bp
    app.register_blueprint(registration_bp)

    return app
