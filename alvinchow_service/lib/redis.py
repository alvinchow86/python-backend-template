from alvinchow.redis.connection import get_connection as _get_connection


def get_redis_connection(connection_alias='default'):
    # Default to the "default" Redis alias
    return _get_connection(connection_alias)
