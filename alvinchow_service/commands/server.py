import click

from alvinchow_service.api.grpc import server as grpc_server
from alvinchow_service.app.flask.server import app as flask_app


@click.command(name='runserver')
@click.option('-h', '--host', default='0.0.0.0')
@click.option('-p', '--port', default=8000)
@click.option('--debug/--no-debug', default=True, envvar='FLASK_DEBUG')
@click.option('--debugger', 'use_debugger', is_flag=True, envvar='FLASK_DEBUGGER')
@click.option('--autoreload/--no-autoreload', default=True, envvar='FLASK_AUTORELOAD')
def run_server(host, port, debug, use_debugger, autoreload):
    print(
        'Running Flask development server on port {} (debug={}, debugger={}, autoreload={})'.format(
            port, debug, use_debugger, autoreload
        )
    )
    flask_app.run(
        host=host,
        port=port,
        debug=True,
        use_debugger=use_debugger,
        use_reloader=autoreload
    )


@click.command(name='rungrpcserver')
@click.option('-p', '--port', default=50051)
def run_grpc_server(port):
    print('Running gRPC server on port {}'.format(port))

    grpc_server.serve(port=port)
