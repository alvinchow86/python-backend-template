from flask import session, g
from alvinchow_backend.service.authentication.login import authenticate_user_with_credentials
from alvinchow_backend.service.authentication.exceptions import AuthenticationError
from alvinchow_backend.db.repository import user_repo


def login_user_with_credentials(email, password, expiration_seconds=None):
    try:
        user = authenticate_user_with_credentials(email, password)
    except AuthenticationError:
        raise

    login_user(user)
    return user


def login_user(user):
    save_user_id_to_session(user)
    g.user = user


def logout_current_user():
    session.clear()
    g.user = None


def save_user_id_to_session(user):
    session['user_id'] = str(user.id)


def get_current_user():
    return g.user


def get_current_user_id_from_session():
    try:
        user_id = int(session['user_id'])
        return user_id
    except KeyError:
        return None


def get_current_user_from_session():
    user_id = get_current_user_id_from_session()
    if user_id:
        user = user_repo.get_user(user_id, raise_exception=None)
        if user:
            return user
