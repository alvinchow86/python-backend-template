# convenience
from alvinchow.sqlalchemy.utils import (  # noqa
    instance_or_id,
    handle_db_not_found,
)

from alvinchow_backend.db.repository.exceptions import UpdateError


def set_write_fields(instance, data):
    for key, val in data.items():
        setattr(instance, key, val)


def validate_write_fields(raw_data, writable_fields, exception_cls=UpdateError):
    write_fields = {}
    for name, value in raw_data.items():
        if name in writable_fields:
            write_fields[name] = value
        else:
            raise exception_cls(f'Cannot write this field {name}')
    return write_fields
