import subprocess

import click
import alembic.config

from alvinchow_backend import app


DB_NAME = 'alvinchow_backend'


@click.group()
def db():
    pass


def run_alembic_command(command):
    args = command.split()
    return alembic.config.main(argv=args)


@click.command()
@click.option('--undo', is_flag=True)
def migrate(undo):
    _migrate_db(undo)


def _migrate_db(undo=False):
    print('--> Migrating database')
    if undo:
        return run_alembic_command('downgrade -1')
    else:
        return run_alembic_command('upgrade head')


@click.command(name='migrationstatus')
def migration_status():
    run_alembic_command('current')


@click.command(name='makemigration')
@click.option('-m', '--message', 'message', required=True)
def make_migration(message):
    command = 'revision --autogenerate'
    if message:
        command += ' -m {}'.format(message)
    run_alembic_command(command)


def _drop_db():
    print('--> Dropping database')
    subprocess.run('dropdb {}'.format(DB_NAME), shell=True, check=True)


def _create_db():
    print('--> Creating database')
    subprocess.run('createdb {}'.format(DB_NAME), shell=True, check=True)


@click.command(name='reset')
@click.option('--drop-db', is_flag=True)
@click.option('--tables/--no-tables', 'create_tables', default=True)
@click.option('--migrate', is_flag=True)
@app.app_context()
def reset_db(drop_db, create_tables, migrate):
    _reset_db(drop_db=drop_db, create_tables=create_tables, migrate=migrate)


def _reset_db(drop_db=False, create_tables=True, migrate=False):
    from alvinchow_backend.db.base import Base, get_engine
    engine = get_engine()
    conn = engine.connect()

    if migrate:
        create_tables = False

    if drop_db:
        _drop_db()
        _create_db()
    else:
        print('--> Dropping tables')
        Base.metadata.drop_all(conn)

        # Clear alembic_version table too
        try:
            conn.execute('drop table alembic_version')
        except Exception:
            pass

    if create_tables:
        print('--> Creating tables')
        Base.metadata.create_all(conn)

    if migrate:
        _migrate_db()


@click.command(name='drop')
def drop_db():
    _drop_db()


@click.command(name='create')
@click.option('--drop', is_flag=True)
def create_db(drop):
    if drop:
        _drop_db()
    _create_db()


db.add_command(migrate)
db.add_command(migration_status)
db.add_command(make_migration)

if not app.config.PRODUCTION:
    db.add_command(reset_db)
    db.add_command(drop_db)
    db.add_command(create_db)
