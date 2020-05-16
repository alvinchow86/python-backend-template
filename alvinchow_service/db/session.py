from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from alvinchow_service.db.exceptions import MutationError
from alvinchow_service.db import base


def get_session():
    return base.Session


def set_session(session):
    base.Session = session


@contextmanager
def session_commit(exception=MutationError):
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        if exception:
            raise exception(str(e))
        else:
            raise


def commit_session_or_raise(session, exception=None):
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise exception(str(e))
