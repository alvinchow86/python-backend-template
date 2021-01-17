from alvinchow_backend.db.session import get_session, session_commit
from alvinchow_backend.db.repository.utils import validate_write_fields, set_write_fields, instance_or_id
from alvinchow_backend.db.repository.exceptions import CreateError, UpdateError
from alvinchow_backend.db.models import User
from alvinchow.sqlalchemy.utils import handle_db_not_found
from alvinchow.lib.dates import utcnow

writable_fields = set(User.get_writable_column_names())


@handle_db_not_found()
def get_user(id) -> User:
    session = get_session()

    user = session.query(User).filter_by(id=id).one()

    return user


@handle_db_not_found()
def get_user_by_email(email) -> User:
    """ Only returns verified user """
    session = get_session()
    user = session.query(User).filter(
        User.email == email,
        User.email_verified_at.isnot(None),
    ).one_or_none()

    return user


def get_user_or_id(user_or_id):
    return instance_or_id(user_or_id, get_user)


def create_user(
    email,
    password=None,
    email_verified_at=None,
    commit=True
) -> User:
    user = User(
        email=email,
        email_verified_at=email_verified_at,
        password=password,
    )
    if password:
        user.password_updated_at = utcnow()

    with session_commit(exception=CreateError, commit=commit) as session:
        session.add(user)

    return user


def update_user(user, commit=True, **fields) -> User:
    write_fields = validate_write_fields(fields, writable_fields)
    with session_commit(exception=UpdateError, commit=commit):
        set_write_fields(user, write_fields)

    return user


def mark_user_email_verified(user, time=None):
    time = time or utcnow()
    if user.email_verified_at:
        raise UpdateError('Already verified')

    update_user(
        user,
        email_verified_at=utcnow(),
    )
    return user
