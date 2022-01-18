from flask import Blueprint

bp = Blueprint('registration', __name__)

from . import routes