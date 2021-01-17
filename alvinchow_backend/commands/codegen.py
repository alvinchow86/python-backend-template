import click

from alvinchow_backend.utils.string import camel_to_snake_case


REPO_TEMPLATE = """
from alvinchow_backend.db.session import get_session, session_commit
from alvinchow_backend.db.repository.utils import validate_write_fields, set_write_fields, instance_or_id
from alvinchow_backend.db.repository.exceptions import CreateError, UpdateError
from alvinchow_backend.db.models import {cls}
from alvinchow.sqlalchemy.utils import handle_db_not_found


writable_fields = set({cls}.get_writable_column_names())


@handle_db_not_found()
def get_{obj}(id) -> {cls}:
    session = get_session()
    {obj} = session.query({cls}).filter_by(id=id).one()
    return {obj}


def get_{obj}_or_id({obj}_or_id):
    return instance_or_id({obj}_or_id, get_{obj})


def create_{obj}(commit=True) -> {cls}:
    {obj} = {cls}()

    with session_commit(exception=CreateError, commit=commit) as session:
        session.add({obj})

    return {obj}


def update_{obj}({obj}, commit=True, **fields) -> {cls}:
    write_fields = validate_write_fields(fields, writable_fields)
    with session_commit(exception=UpdateError, commit=commit):
        set_write_fields({obj}, write_fields)

    return {obj}


def delete_{obj}({obj}):
    with session_commit() as session:
        session.delete({obj})


""".lstrip()


@click.command(name='genrepocode')
@click.option('-m', '--module')
@click.argument('classname')
def gen_repo_code(classname, module):
    object_snake = camel_to_snake_case(classname)

    content = REPO_TEMPLATE.format(
        obj=object_snake,
        cls=classname
    )
    print('-----START--------')
    print(content)
    print('-----END--------')
    print()

    if module:
        filepath = f'alvinchow_backend/db/repository/{module}.py'
        click.confirm(f'--> Write to this file {filepath}?', abort=True)
        with open(filepath, 'w') as f:
            f.write(content)
