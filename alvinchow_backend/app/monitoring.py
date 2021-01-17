import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from alvinchow_backend.app import config


def initialize_sentry(flask=False, celery=False):  # pragma: no cover
    if not config.SENTRY_DSN:
        return

    integrations = [SqlalchemyIntegration(), RedisIntegration()]
    if flask:
        integrations.append(FlaskIntegration())
    if celery:
        integrations.append(CeleryIntegration())

    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        integrations=integrations,
        environment=config.APP_ENV,
    )
