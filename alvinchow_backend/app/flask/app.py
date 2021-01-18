from flask import Flask, jsonify, request, session
from flask_cors import CORS

from scout_apm.flask import ScoutApm

from alvinchow_backend.api.rest import api
from alvinchow_backend.app import config
from alvinchow_backend.app import initialize

from alvinchow_backend.app.flask.csrf import register_csrf
from alvinchow_backend.app.flask.middleware import process_user_from_session
from alvinchow_backend.app.flask.session import RedisSessionInterface
from alvinchow_backend.app.monitoring import initialize_sentry
from alvinchow_backend.api.graphql.view import create_graphql_view
from alvinchow_backend.db import get_session
from alvinchow_backend.lib.web import exceptions
from alvinchow_backend.lib import get_logger
from alvinchow_backend.web import web

logger = get_logger(__name__)


CSRF_EXCLUDE_PATTERN = None
if not config.PRODUCTION:
    CSRF_EXCLUDE_PATTERN = '/dev'


def create_app():
    initialize()
    # App initialization code goes here
    app = Flask(__name__)

    common_app_setup(app)

    # Handle user sessions
    app.before_request(process_user_from_session)

    # Register csrf everywhere
    register_csrf(app, exclude_url_pattern=CSRF_EXCLUDE_PATTERN)

    # Register blueprints/views
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(web)

    app.add_url_rule(
        '/api/graphql',
        view_func=create_graphql_view()
    )

    return app


def common_app_setup(app, session_cookie_domain=None, session_expiration_seconds=None):
    app.session_interface = RedisSessionInterface(
        session_cookie_domain=session_cookie_domain,
        session_expiration_seconds=session_expiration_seconds,
    )

    CORS(app, supports_credentials=config.CORS_SUPPORT_CREDENTIALS)

    register_global_endpoints(app)
    register_request_cleanup(app)
    register_request_handlers(app)

    initialize_sentry(flask=True)

    if config.SCOUT_KEY:
        app.config['SCOUT_MONITOR'] = True
        app.config['SCOUT_KEY'] = config.SCOUT_KEY
        app.config['SCOUT_NAME'] = config.SCOUT_NAME
        app.config['SCOUT_CORE_AGENT_FULL_NAME'] = "scout_apm_core-v1.1.8-x86_64-unknown-linux-musl"

        ScoutApm(app)

    app.config['SESSION_COOKIE_NAME'] = 'session_id'


def register_global_endpoints(app):
    @app.route('/health')
    def health():
        return 'OK'

    @app.route('/debug')
    def debug_request():
        result = {}
        result.update(headers=dict(request.headers.items()))
        return jsonify(result)

    @app.route('/sentry-test')
    def exception():
        5 / 0

    if not config.PRODUCTION:
        @app.route('/debug/session')
        def debug_session():
            session_data = dict(session)
            return jsonify(**session_data)


def register_request_cleanup(app):
    @app.after_request
    def db_conn_cleanup(response):
        session = get_session()
        session.remove()
        return response


def register_request_handlers(app):
    @app.errorhandler(exceptions.ApiException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
