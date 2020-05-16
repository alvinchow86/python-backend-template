from alvinchow.lib.dates import utcnow

from alvinchow_service.lib.celery import task
from alvinchow_service.lib.logger import get_logger


logger = get_logger(__name__)


@task
def heartbeat():
    logger.info('Heartbeat %s', utcnow())
