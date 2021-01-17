from alvinchow_backend.service.authentication.password import verify_password
from alvinchow_backend.service.authentication.exceptions import AuthenticationError
from alvinchow_backend.db.repository import user_repo


def authenticate_user_with_credentials(email, password):
    user = user_repo.get_user_by_email(email)
    if not user:
        raise AuthenticationError(code=AuthenticationError.USER_NOT_FOUND)

    password_matches = verify_password(password, user.password)
    if not password_matches:
        raise AuthenticationError(code=AuthenticationError.INVALID_CREDENTIALS)

    return user
