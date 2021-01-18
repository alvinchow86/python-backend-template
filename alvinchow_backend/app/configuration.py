import os

from alvinchow.lib.config import Configuration
from alvinchow.lib.config.values import Value, BooleanValue, IntegerValue


class Base(Configuration):
    DEBUG_LEVEL = Value('INFO')
    ENV = Value('local')

    DOMAIN = Value('alvinchow.localdev')
    SESSION_COOKIE_DOMAIN = Value()
    SESSION_COOKIE_NAME = Value('session_id')
    SESSION_COOKIE_SECURE = BooleanValue(False)
    CSRF_COOKIE_DOMAIN = Value()
    CSRF_ENABLED = BooleanValue(True)
    CORS_SUPPORT_CREDENTIALS = BooleanValue(False)

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
    DEVELOPMENT = False
    PRODUCTION = False
    ENV_TYPE = None

    def setup(self):  # pragma: no cove
        super().setup()

        self.CELERY_BROKER_URL = self.CELERY_BROKER_URL or '{}/0'.format(self.REDIS_URL)


class DevelopmentTestingBase(Base):
    USE_LOCAL_CONFIG = BooleanValue(True)

    def setup(self):  # pragma: no cover
        super().setup()

        if self.USE_LOCAL_CONFIG:
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


class Development(DevelopmentTestingBase):
    ENV_TYPE = 'development'

    REQUIRE_STRONG_PASSWORDS = BooleanValue(False)
    CORS_SUPPORT_CREDENTIALS = BooleanValue(True)
    CSRF_ENABLED = BooleanValue(False)
    DEVELOPMENT = True
    CORS_SUPPORT_CREDENTIALS = BooleanValue(True)


class Testing(DevelopmentTestingBase):
    ENV_TYPE = 'testing'
    TESTING = True
    CELERY_TASK_ALWAYS_EAGER = True

    # By default do not read from local_config.py in tests
    USE_LOCAL_CONFIG = BooleanValue(False)


class Deployed(Base):
    pass


class Staging(Deployed):
    ENV_TYPE = 'staging'
    ENV = Value('staging')


class Production(Deployed):
    ENV_TYPE = 'production'
    ENV = Value('production')
    PRODUCTION = True
    DEBUG_SQL = False

    CSRF_ENABLED = True
    CORS_SUPPORT_CREDENTIALS = False


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
