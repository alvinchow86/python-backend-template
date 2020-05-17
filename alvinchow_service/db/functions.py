from sqlalchemy import event

from sqlalchemy_bigid import register_nextbigid_function


def register_postgres_functions(metadata):
    register_nextbigid_function(metadata)
