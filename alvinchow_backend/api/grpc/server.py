from concurrent import futures
import time

import grpc
import scout_apm.api

from alvinchow_backend import app
from alvinchow_backend.app import config
from alvinchow_backend.app.monitoring import initialize_sentry
from alvinchow_backend.api.grpc.endpoints import AlvinChowServiceServicer
from alvinchow_backend_protobuf import alvinchow_backend_pb2_grpc
from alvinchow_backend.api.grpc.interceptors import DefaultInterceptor
from alvinchow_backend.lib import get_logger


logger = get_logger(__name__)


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


DEFAULT_NUM_WORKERS = 16


def create_grpc_server(address='[::]:50051', num_workers=DEFAULT_NUM_WORKERS):
    app.initialize()

    if config.SCOUT_KEY:  # pragma: no cover
        scout_config = {
            'name': config.SCOUT_NAME,
            'key': config.SCOUT_KEY,
            'monitor': True,
            'core_agent_full_name': "scout_apm_core-v1.1.8-x86_64-unknown-linux-musl"
        }
        scout_apm.api.install(config=scout_config)

    default_interceptor = DefaultInterceptor()

    pool = futures.ThreadPoolExecutor(max_workers=num_workers)
    options = (
        ('grpc.keepalive_permit_without_calls', True),
        ('grpc.http2.max_pings_without_data', 0),
        ('grpc.http2.min_time_between_pings_ms', 1000),
        ('grpc.http2.min_ping_interval_without_data_ms', 1000),
        ('grpc.http2.max_ping_strikes', 0),
    )

    server = grpc.server(pool, interceptors=(default_interceptor,), options=options)

    alvinchow_backend_pb2_grpc.add_AlvinChowServiceServicer_to_server(
        AlvinChowServiceServicer(), server
    )
    server.add_insecure_port(address)

    initialize_sentry()

    return server


def serve(address=None, host='[::]', port=50051, num_workers=DEFAULT_NUM_WORKERS):
    address = address or '{}:{}'.format(host, port)

    server = create_grpc_server(address, num_workers=num_workers)
    print('gRPC server starting (address: {}, workers={})'.format(address, num_workers))
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
        print('Stopped gRPC server')


if __name__ == '__main__':
    serve()
