from flask import current_app, request, make_response, jsonify
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from . import bp
from ..models import db
from .utils import CreateUserService, UserConfirmationService, ConfirmationService
from ..validators import RegistrationForm


@bp.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm.parse_raw(request.data)
    service = CreateUserService(form)
    if service.already_exist():
        response = make_response(
            jsonify(
                {"message": "User with that name or email already exists"}
            ),
            422,
        )
        response.headers["Content-Type"] = "application/json"
        return response
    user = service.create_user_for_registration()
    try:
        db.session.add(user)
        db.session.commit()

        current_app.logger.info(f"add user: {user.id}, {user.username}, {user.email}")

    except SQLAlchemyError:
        response = make_response(
            jsonify(
                {"message": "Internal Server Error"}
            ),
            500,
        )
        response.headers["Content-Type"] = "application/json"
        return response
    confirmation = UserConfirmationService(user)
    confirmation.send_confirmation(email=user.email, token=user.token, base_url=request.url_root)
    return {
        "created":
            {
                "username": user.username,
                "email": user.email
            },
        "message": "Confirmation message sent. Please, check your email and follow the link."

    }


@bp.route('/confirm', methods=['GET'])
def confirm():
    cur_token = request.args.get('token', '')
    if cur_token == '':
        response = make_response(
            jsonify(
                {"message": "Bad request"}
            ),
            400,
        )
        response.headers["Content-Type"] = "application/json"
        return response
    confirmation = ConfirmationService(cur_token)

    try:
        user = confirmation.get_user()
        cur_mail = confirmation.get_email_from_token()
        if cur_mail != user.email:
            raise NameError
        user.confirmed = True
        db.session.commit()
    except NameError:
        response = make_response(jsonify({"message": "Bad request. Wrong Email"}), 400)
        response.headers["Content-Type"] = "application/json"
        return response
    except NoResultFound:
        response = make_response(jsonify({"message": "User with that email not found. Please, register"}), 404)
        response.headers["Content-Type"] = "application/json"
        return response

    response = make_response(jsonify({"message": "Confirmed! You have the access for your account now."}), 200)
    response.headers["Content-Type"] = "application/json"
    return response
