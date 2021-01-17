from alvinchow_backend.service.user.creation import create_user
from alvinchow_backend.utils.string import random_string


def make_user(email=None, password='alvintester', **fields):
    email = email or '{}@alvinchow.com'.format(random_string(12))
    user = create_user(email, password, email_verified=True, **fields)
    return user
