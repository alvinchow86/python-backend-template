from sqlalchemy import event

from alvinchow.sqlalchemy.bigid.schema import create_function_nextbigid


def register_postgres_functions(metadata):
    event.listen(metadata, 'before_create', create_function_nextbigid)
