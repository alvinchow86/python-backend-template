import logging.config
import sys

from alvinchow_backend.app.configuration import config


DEBUG_LEVEL = config.DEBUG_LEVEL
CELERY_DEBUG_LEVEL = config.CELERY_DEBUG_LEVEL


logging_config = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        # for Celery internal messages, use slightly modified version (no line number)
        'celery': {
            'format': "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': "[%(asctime)s] [%(levelname)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout
        },
        'console_celery': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'celery',
            'stream': sys.stdout
        },
        'console_simple': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout
        },
    },
    'loggers': {
        'werkzeug': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'alvinchow': {
            'handlers': ['console'],
            'level': DEBUG_LEVEL,
            'propagate': False,
        },
        'alvinchow_backend': {
            'handlers': ['console'],
            'level': DEBUG_LEVEL,
            'propagate': False,
        },
        # special name for grpc api request logging
        'grpc_request': {
            'handlers': ['console_simple'],
            'level': DEBUG_LEVEL,
            'propagate': False,
        },
        'celery': {
            'handlers': ['console_celery'],
            'level': CELERY_DEBUG_LEVEL,
            'propagate': False,
        },
        'scout_apm': {
            'handlers': ['console'],
            'level': config.SCOUT_DEBUG_LEVEL,
            'propagate': False,
        },
    },
}


def setup_logging():
    logging.config.dictConfig(logging_config)
