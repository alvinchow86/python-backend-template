from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from scout_apm.sqlalchemy import instrument_sqlalchemy
import sqlalchemy_bigint_id

from alvinchow_backend.app import config


BIGINT_ID_EPOCH_SECONDS = 1589674264    # this is 1/1/2020, configure to whatever you like


Base = declarative_base()     # this is used for models
sqlalchemy_bigint_id.configure(epoch_seconds=BIGINT_ID_EPOCH_SECONDS)


engine = None
Session = None


def initialize_database(database_url=None):
    global engine, Session
    from alvinchow_backend.db import functions  # noqa

    database_url = database_url or config.DATABASE_URL

    connection_args = {
        'connect_args': {
            'connect_timeout': 10
        }
    }

    if config.DEBUG_SQL:
        connection_args.update({'echo': True})

    engine = create_engine(database_url, **connection_args)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)

    # import models to register them here
    from alvinchow_backend.db import models   # noqa
    from sqlalchemy_bigint_id import setup_bigint_id_for_all_tables

    functions.register_postgres_functions(metadata=Base.metadata)

    # Register bigid for all tables that have it
    setup_bigint_id_for_all_tables(metadata=Base.metadata)

    instrument_sqlalchemy(engine)


def get_engine():
    return engine
