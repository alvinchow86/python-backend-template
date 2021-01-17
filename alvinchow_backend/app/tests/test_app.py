"""
Test some basic things in "app" package
"""
from celery import Celery

from alvinchow_backend import app
from alvinchow_backend.app import initialization, scheduler, worker


def test_app():
    app.initialize()
    assert initialization.is_initialized()
    app.initialize()


def test_app_content():
    with app.app_context():
        print('within app context')


def test_scheduler():
    # Just test that initializing scheduler works
    assert scheduler.scheduler


def test_worker():
    assert isinstance(worker.app, Celery)
