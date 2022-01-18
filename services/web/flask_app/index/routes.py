from flask import jsonify

from . import bp


@bp.route("/")
def index():
    msg = [
        {"message": "Hello, World!"}
    ]
    return jsonify(msg)
