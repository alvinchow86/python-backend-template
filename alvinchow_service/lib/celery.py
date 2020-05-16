from alvinchow_service.app.celery import app


# Set up task decorator to be registered to our Celery app
task = app.task   # noqa
