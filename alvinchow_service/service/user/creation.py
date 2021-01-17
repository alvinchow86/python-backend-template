from alvinchow_service.app import config
from alvinchow_service.db.repository import user_repo
from alvinchow_service.authentication.password import hash_password, check_password_strength
from alvinchow.lib.dates import utcnow


def create_user(email, password=None, email_verified=False, **fields):
    args = dict(
        email=email
    )
    args.update(fields)
    if password:
        password_hash = hash_password(password)
        args.update(password=password_hash)

    if email_verified:
        args.update(email_verified_at=utcnow())

    user = user_repo.create_user(
        **args
    )

    return user


def create_user_flow(email, password=None):
    user = create_user(email, password=password)

    # Send email verification

    return user
