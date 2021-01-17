
from functools import wraps

from alvinchow_backend.lib.web.exceptions import UnauthorizedError
from alvinchow_backend.lib.web.user import get_current_user


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        current_user = get_current_user()
        if not current_user:
            raise UnauthorizedError()
        return f(*args, **kwargs)

    return wrapped
