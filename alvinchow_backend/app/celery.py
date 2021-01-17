from celery import Celery
from celery.signals import task_postrun

from alvinchow_backend.app.configuration import config


include_modules = [
    'alvinchow_backend.tasks',
]


celery_config = dict(
    task_default_queue='default',
    task_ignore_result=True,
    worker_hijack_root_logger=False,
    worker_redirect_stdouts_level='INFO',
    task_time_limit=config.CELERY_TASK_TIME_LIMIT,
    task_always_eager=config.CELERY_TASK_ALWAYS_EAGER,
    task_eager_propagates=config.CELERY_TASK_ALWAYS_EAGER,
)


app = Celery(
    'celery',
    broker=config.CELERY_BROKER_URL,
    include=include_modules
)


app.conf.update(**celery_config)


@task_postrun.connect
def task_postrun_handler(sender=None, headers=None, body=None, **kwargs):
    from alvinchow_backend.db import get_session
    if config.TESTING:
        # Don't do this in unit tests since Celery runs eagerly
        return

    # Clear DB session between tasks
    session = get_session()
    session.remove()
