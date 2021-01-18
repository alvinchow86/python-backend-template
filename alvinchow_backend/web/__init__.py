from flask import Blueprint


web = Blueprint(
    'web', __name__,
    template_folder='templates',
    root_path='alvinchow_backend/web',
)

from . import development  # noqa
