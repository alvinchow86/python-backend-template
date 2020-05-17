from sqlalchemy import event

from sqlalchemy_bigid import create_function_nextbigid


def register_postgres_functions(metadata):
    event.listen(metadata, 'before_create', create_function_nextbigid)
