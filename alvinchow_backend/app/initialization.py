import pkg_resources     # noqa: for some reason need this for "import google.protobuf" to work properly
from contextlib import ContextDecorator

from alvinchow_backend.app import celery    # noqa  # make sure Celery is loaded
from alvinchow_backend.app.configuration import config    # noqa
from alvinchow_backend.app.logging import setup_logging
from alvinchow_backend.app.redis import setup_redis
from alvinchow_backend.db.base import initialize_database
from alvinchow_backend.lib.logger import get_logger


logger = get_logger(__name__)

_app_initialized = False


def initialize(force=False):
    """
    Configure stuff on app startup
    """
    global _app_initialized

    if _app_initialized and not force:
        return

    setup_logging()
    initialize_database()
    setup_redis()

    logger.debug('App initialized')

    _app_initialized = True


def is_initialized():
    return _app_initialized


class app_context(ContextDecorator):
    """
    Use this a decorator or context manager
    """
    def __enter__(self):
        initialize()
        return self

    def __exit__(self, *exc):
        pass
