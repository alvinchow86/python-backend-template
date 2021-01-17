from alvinchow.redis.connection import get_connection as _get_connection
from alvinchow.redis.cache import get_cache as _get_cache


def get_redis_connection(connection_alias='default'):
    # Default to the "default" Redis alias
    return _get_connection(connection_alias)


def get_default_redis_connection():
    return get_redis_connection('default')


def get_session_redis_connection():
    return _get_connection('default')


def get_cache():
    return _get_cache('default')
