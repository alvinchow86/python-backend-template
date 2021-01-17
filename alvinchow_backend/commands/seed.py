import click

from alvinchow_backend import app
from alvinchow_backend.service.user.creation import create_user as _create_user
from alvinchow_backend.commands.db import _reset_db


env = app.config.APP_ENV


@click.group()
def seed():
    pass


@seed.command(name='local')
@click.option('--reset-db', is_flag=True)
@click.option('--no-migrate', is_flag=True)
@click.option('--no-docs', is_flag=True)
@app.app_context()
def seed_local(reset_db, no_migrate=False, no_docs=False):
    migrate = not no_migrate
    if reset_db:
        _reset_db(migrate=migrate)
    print('--> Seeding')
    # Add  local seed script stuff here


@click.command(name='makeuser')
@click.argument('email')
@click.argument('password')
@app.app_context()
def make_user(email, password):
    _create_user(email, password)
