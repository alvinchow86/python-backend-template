from alvinchow_backend.lib.exceptions import BaseException


class AuthenticationError(BaseException):
    USER_NOT_FOUND = 'user_not_found'
    INVALID_CREDENTIALS = 'invalid_credentials'


class InvalidLoginSession(BaseException):
    pass
