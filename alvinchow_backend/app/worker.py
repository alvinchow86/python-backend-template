"""
Celery worker entry point
"""
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
import scout_apm.api
import scout_apm.celery

from alvinchow_backend.app.celery import app   # noqa, this module needs "app"
from alvinchow_backend.app import config, initialize
from alvinchow_backend.app.monitoring import initialize_sentry


initialize()
initialize_sentry(celery=True)


if config.SENTRY_DSN:  # pragma: no cover
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
        integrations=[CeleryIntegration()]
    )


if config.SCOUT_KEY:  # pragma: no cover
    scout_apm.api.Config.set(
        key=config.SCOUT_KEY,
        name=config.SCOUT_NAME,
        monitor=True,
        full_name="scout_apm_core-v1.1.8-x86_64-unknown-linux-musl",
    )

    scout_apm.celery.install()
