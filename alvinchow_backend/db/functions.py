from sqlalchemy_bigint_id import register_next_bigint_id_function


def register_postgres_functions(metadata):
    register_next_bigint_id_function(metadata)
