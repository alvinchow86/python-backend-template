#!/usr/bin/env python3
import click
import os
import json
from easydict import EasyDict
import yaml
import jinja2


ENVS = ['production', 'staging']


root = os.path.dirname(os.path.abspath(__file__))


@click.group()
def cli():
    pass


@cli.command(name='taskdefs')
@click.argument('envs', nargs=-1)
def build_task_defs(envs):
    envs = envs or ENVS
    for env in envs:
        compile_task_def_for_env(env)


@cli.command(name='buildspecs')
@click.argument('envs', nargs=-1)
def compile_buildspecs(envs):
    envs = envs or ENVS
    for env in ENVS:
        compile_buildspec_for_env(env)


def compile_task_def_for_env(env):
    """
    - env: "production", "staging", etc
    """
    print('--> Compiling task defs for {}'.format(env))

    src_path = os.path.join(root, f'{env}/src')
    service_yaml_path = os.path.join(src_path, 'services.yaml')
    env_yaml_path = os.path.join(src_path, 'env.yaml')

    service_data = yaml.load(open(service_yaml_path).read(), Loader=yaml.FullLoader)
    services = service_data['services']
    execution_role = service_data['execution_role']
    image = service_data['image']
    task_role = service_data.get('task_role')

    env_data = yaml.load(open(env_yaml_path).read(), Loader=yaml.FullLoader)
    env_vars = env_data['env_vars']
    secrets = env_data['secrets']

    for service in services:
        target_filename = os.path.join(root, env, service['file'])
        data = create_task_definition_dict(
            execution_role=execution_role,
            task_role=task_role,
            image=image,
            env_vars=env_vars,
            secrets=secrets,
            **service
        )
        output = json.dumps(data, indent=2) + '\n'

        with open(target_filename, 'w') as f:
            f.write(output)


def create_task_definition_dict(
    family,
    execution_role,
    image,
    env_vars,
    secrets,
    container_name,
    command,
    cpu,
    memory,
    task_role=None,
    ports=None,
    **kwargs,
):
    ports = ports or []
    env_vars = env_vars or []
    secrets = secrets or []

    d = EasyDict()
    d.update(
        family=family,
        executionRoleArn=execution_role,
    )
    if task_role:
        d.taskRoleArn = task_role

    container = EasyDict()
    container.name = container_name
    container.image = image
    container.memoryReservation = memory

    port_mappings = [
        {
            'containerPort': port,
            'hostPort': 0,
            'protocol': 'tcp',
        } for port in ports
    ]

    container.portMappings = port_mappings
    container.command = [command]
    container.environment = [dict(name=name, value=value) for (name, value) in env_vars.items()]
    container.secrets = [dict(name=name, valueFrom=value) for (name, value) in secrets.items()]
    container.logConfiguration = dict(logDriver="json-file")
    d.containerDefinitions = [container]

    d.cpu = str(cpu)
    d.memory = str(memory)
    d.requiresCompatibilities = ['EC2']
    return d


def compile_buildspec_for_env(env):
    print('--> Compiling buildspecs for {}'.format(env))
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([
            os.path.join(root, 'common'),
            os.path.join(root, f'{env}/src'),
        ]),
        keep_trailing_newline=True,
    )
    output_path = os.path.join(root, env, 'buildspec.yml')

    template = jinja_env.get_template('buildspec.jinja.yml')
    data = template.render()

    with open(output_path, 'w') as f:
        f.write(data)


if __name__ == '__main__':
    cli()
