from flask import g

from alvinchow_backend.lib.web.user import get_current_user_from_session


def process_user_from_session():
    user = get_current_user_from_session()
    if user:
        g.user = user
    else:
        g.user = None
