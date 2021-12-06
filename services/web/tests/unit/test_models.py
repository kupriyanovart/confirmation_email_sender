from services.web.flask_app.models import User


def test_new_user_password():
    username = "artem"
    email = "123@gmail.com"
    password = "123strong"
    token = "123token123"
    user = User(username=username, email=email, token=token)
    user.set_password(password)
    assert user.password_hash != password
    assert user.check_password(password)
    assert user.token
    assert not user.check_password("123weak")
    assert not user.is_authenticated()
