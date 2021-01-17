import traceback
from alvinchow.grpc.server.error_handling import create_grpc_error_handler
import sentry_sdk

from alvinchow_backend.lib import get_logger

logger = get_logger(__name__)


def on_uncaught_exception(e):
    logger.warning('Uncaught exception: %s', e)
    logger.warning('%s', traceback.format_exc())
    sentry_sdk.capture_exception(e)


handle_grpc_errors = create_grpc_error_handler(on_uncaught_exception=on_uncaught_exception)
