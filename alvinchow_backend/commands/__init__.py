import click

from alvinchow_backend.commands.db import db
from alvinchow_backend.commands.server import run_server, run_grpc_server


@click.group()
def cli():
    pass


cli.add_command(db)
cli.add_command(run_server)
cli.add_command(run_grpc_server)
