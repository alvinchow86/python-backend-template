from flask import Flask, jsonify, request
from scout_apm.flask import ScoutApm
import sentry_sdk

from alvinchow_service.api.rest import api
from alvinchow_service.app import config
from alvinchow_service.app import initialize
from alvinchow_service.app.flask.csrf import set_csrf_cookie_on_response, csrf_protect_request
from alvinchow_service.db import get_session
# from alvinchow_service.web import web
from alvinchow_service.api.rest import exceptions
from alvinchow_service.lib import get_logger

logger = get_logger(__name__)


def create_app():
    initialize()
    # App initialization code goes here
    app = Flask(__name__)

    if config.SENTRY_DSN:
        sentry_sdk.init(
            dsn=config.SENTRY_DSN,
        )

    app.register_blueprint(api, url_prefix='/api')
    # app.register_blueprint(web)

    @app.errorhandler(exceptions.APIException)
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

    # CSRF (remove if not using csrf/app is not serving web clients)
    app.before_request(csrf_protect_request)
    app.after_request(set_csrf_cookie_on_response)

    if config.SCOUT_KEY:
        app.config['SCOUT_MONITOR'] = True
        app.config['SCOUT_KEY'] = config.SCOUT_KEY
        app.config['SCOUT_NAME'] = config.SCOUT_NAME
        app.config['SCOUT_CORE_AGENT_FULL_NAME'] = "scout_apm_core-v1.1.8-x86_64-unknown-linux-musl"

        ScoutApm(app)

    return app
