import click

from alvinchow_service.api.grpc import server as grpc_server


@click.command(name='rungrpcserver')
@click.option('-p', '--port', default=50051)
def run_grpc_server(port):
    print('Running gRPC server on port {}'.format(port))

    grpc_server.serve(port=port)
