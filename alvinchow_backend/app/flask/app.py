from flask import Flask, jsonify, request
from scout_apm.flask import ScoutApm

from alvinchow_backend.api.rest import api
from alvinchow_backend.app import config
from alvinchow_backend.app import initialize
from alvinchow_backend.app.flask.csrf import register_csrf
from alvinchow_backend.app.flask.session import RedisSessionInterface
from alvinchow_backend.app.monitoring import initialize_sentry

from alvinchow_backend.db import get_session
from alvinchow_backend.lib.web import exceptions
from alvinchow_backend.lib import get_logger

logger = get_logger(__name__)


CSRF_EXCLUDE_PATTERN = None
if not config.PRODUCTION:
    CSRF_EXCLUDE_PATTERN = '/dev'


def create_app():
    initialize()
    # App initialization code goes here
    app = Flask(__name__)

    app.session_interface = RedisSessionInterface()

    app.register_blueprint(api, url_prefix='/api')
    # app.register_blueprint(web)

    app.config['SESSION_COOKIE_NAME'] = 'session_id'

    @app.errorhandler(exceptions.ApiException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # Health check
    @app.route('/')
    def hello():
        return 'Hello world'

    # Health check
    @app.route('/health')
    def health():
        return 'OK'

    @app.route('/debug')
    async def debug_request():
        result = {}
        result.update(headers=dict(request.headers.items()))
        return jsonify(result)

    @app.after_request
    def db_conn_cleanup(response):
        session = get_session()
        session.remove()
        return response

    # Register csrf everywhere
    register_csrf(app, exclude_url_pattern=CSRF_EXCLUDE_PATTERN)

    initialize_sentry(flask=True)

    if config.SCOUT_KEY:
        app.config['SCOUT_MONITOR'] = True
        app.config['SCOUT_KEY'] = config.SCOUT_KEY
        app.config['SCOUT_NAME'] = config.SCOUT_NAME
        app.config['SCOUT_CORE_AGENT_FULL_NAME'] = "scout_apm_core-v1.1.8-x86_64-unknown-linux-musl"

        ScoutApm(app)

    return app
