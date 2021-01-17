from alvinchow.lib.dates import utcnow

from alvinchow_backend.lib.celery import task
from alvinchow_backend.lib.logger import get_logger


logger = get_logger(__name__)


@task
def heartbeat():
    logger.info('Heartbeat %s', utcnow())
