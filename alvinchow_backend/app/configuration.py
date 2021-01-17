import os

from alvinchow.lib.config import Configuration
from alvinchow.lib.config.values import Value, BooleanValue, IntegerValue


class Base(Configuration):
    DEBUG_LEVEL = Value('INFO')
    ENV = Value('local')

    DOMAIN = Value('alvinchow.localdev')
    SESSION_COOKIE_DOMAIN = Value()
    SESSION_COOKIE_SECURE = BooleanValue(False)
    CSRF_COOKIE_DOMAIN = Value()
    ROOT_DOMAIN = Value('alvinchow.localdev')

    STATIC_BASE_URL = Value('/static')

    DATABASE_URL = Value('postgres://root:@postgres/alvinchow_backend')
    REDIS_URL = Value('redis://redis:6379')

    CELERY_BROKER_URL = Value('redis://redis:6379/0')
    CELERY_TASK_TIME_LIMIT = IntegerValue(60)
    CELERY_TASK_ALWAYS_EAGER = False

    DEBUG_SQL = BooleanValue(False)
    CELERY_DEBUG_LEVEL = Value('INFO')

    # Monitoring
    SENTRY_DSN = Value()
    SCOUT_KEY = Value()
    SCOUT_NAME = Value()
    SCOUT_DEBUG_LEVEL = Value('INFO')

    # Useful flags
    TESTING = False
    PRODUCTION = False


class Development(Base):

    def setup(self):  # pragma: no cover
        super().setup()

        # Override settings with a "local_config.py" file
        try:
            import local_config
            local_keys = []

            for key, val in vars(local_config).items():
                if key.upper() == key:
                    setattr(self, key, val)
                    local_keys.append(key)
            print('Overriding config with local_config.py:', local_keys)
        except ImportError:
            pass


class Testing(Base):
    TESTING = True
    CELERY_TASK_ALWAYS_EAGER = True


class Deployed(Base):
    pass


class Staging(Deployed):
    ENV = Value('staging')


class Production(Deployed):
    ENV = Value('production')
    PRODUCTION = True
    DEBUG_SQL = False


app_env = os.environ.get("APP_ENV", 'development')

config_class = {
    'development': Development,
    'testing': Testing,
    'staging': Staging,
    'production': Production,
}.get(app_env, Base)


config = config_class()
config.setup()


# Quick hack to get store APP_ENV somewhere
config.APP_ENV = app_env
