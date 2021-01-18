from alvinchow_backend.app import config
from alvinchow_backend.db.repository import user_repo
from alvinchow_backend.service.authentication.password import hash_password, check_password_strength
from alvinchow.lib.dates import utcnow


def update_user_password(user, password):
    if config.REQUIRE_STRONG_PASSWORDS:
        check_password_strength(password)

    password_hash = hash_password(password)
    user_repo.update_user(user, password=password_hash, password_updated_at=utcnow())
    return user
