from alvinchow_backend.app import config
from alvinchow.redis.connection import configure_connection


def setup_redis():
    default_redis_alias = 'default'

    configure_connection(
        default_redis_alias,
        url=config.REDIS_URL
    )
