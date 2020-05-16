import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from alvinchow_service.app import config


def initialize_sentry(celery=False):  # pragma: no cover
    if not config.SENTRY_DSN:
        return

    integrations = [SqlalchemyIntegration(), RedisIntegration()]
    if celery:
        integrations.append(CeleryIntegration)

    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        integrations=[CeleryIntegration(), SqlalchemyIntegration(), RedisIntegration()],
        environment=config.APP_ENV,
    )
