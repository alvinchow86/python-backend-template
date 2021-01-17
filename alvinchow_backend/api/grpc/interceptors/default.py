import scout_apm.api

from alvinchow_backend.app import config
from alvinchow_backend.lib import get_logger
from alvinchow_backend.db import get_session
from alvinchow.grpc.server.interceptors import DefaultInterceptor as _DefaultInterceptor


grpc_logger = get_logger('grpc_request')


def cleanup_sqlalchemy_session():
    session = get_session()
    session.remove()


SCOUT_ENABLED = bool(config.SCOUT_KEY)


class DefaultInterceptor(_DefaultInterceptor):
    def before_request(self, request_info, *args, **kwargs):
        method_name = request_info['method_name']
        if SCOUT_ENABLED:  # pragma: no cover
            scout_apm.api.WebTransaction.start(method_name)

    def after_request(self, request_info, *args, **kwargs):
        cleanup_sqlalchemy_session()
        if SCOUT_ENABLED:  # pragma: no cover
            scout_apm.api.WebTransaction.stop()
