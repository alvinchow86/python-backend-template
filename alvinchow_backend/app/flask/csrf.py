import secrets
import re

from flask import g, request

from alvinchow_backend.app import config
from alvinchow_backend.app.flask.exceptions import CSRFValidationError
from alvinchow_backend.lib.web import exceptions as api_exceptions
from alvinchow_backend.lib import get_logger

logger = get_logger(__name__)


CSRF_COOKIE_DOMAIN = config.CSRF_COOKIE_DOMAIN
CSRF_COOKIE_NAME = 'csrf_token'
CSRF_TOKEN_NAME = 'csrf_token'
CSRF_COOKIE_MAX_AGE_SECONDS = 3600 * 24
CSRF_HEADER_NAMES = ('CSRF-Token', 'X-CSRF-Token')   # TODO multiple headers


def register_csrf(app_or_blueprint, include_url_pattern: str = None, exclude_url_pattern: str = None):
    """
    Register csrf for a Flask app or blueprint
    """
    csrf_protect_request = create_csrf_protect_request_func(
        include_url_pattern=include_url_pattern,
        exclude_url_pattern=exclude_url_pattern,
    )

    app_or_blueprint.before_request(csrf_protect_request)
    app_or_blueprint.after_request(set_csrf_cookie_on_response)


def create_csrf_protect_request_func(include_url_pattern: str = None, exclude_url_pattern: str = None):
    """
    This is a factory function, so we can have customized CSRF behavior for different Flask apps
    """
    include_url_regex = re.compile(include_url_pattern) if include_url_pattern else None
    exclude_url_regex = re.compile(exclude_url_pattern) if exclude_url_pattern else None

    def csrf_protect_request():
        """
        @app.before_request handler
        """
        if not config.CSRF_ENABLED:
            return

        # Either get the csrf_token from cookie, or make a new one
        csrf_token = _get_csrf_token_from_cookie()
        csrf_token = csrf_token or generate_csrf_token()

        # Pass this to set_csrf_cookie_on_response handler, so it'll know to set the response cookie
        # we set it here so we have the ability to unset/reset the token if we need to
        g.csrf_token = csrf_token

        # Include or exclude certain routes
        path = request.path
        if include_url_regex and not include_url_regex.match(path):
            return

        if exclude_url_regex and exclude_url_regex.match(path):
            return

        if request.method in ("POST", "PATCH", "PUT", "DELETE"):
            try:
                verify_csrf()
            except CSRFValidationError:
                logger.debug('CSRF verification failed')
                raise api_exceptions.CSRFValidationError('CSRF validation failed', error_code='csrf_validation_failed')

    return csrf_protect_request


def set_csrf_cookie_on_response(response):
    csrf_token = get_current_csrf_token()
    if not csrf_token:
        logger.debug('No CSRF token, making new one')
        csrf_token = generate_csrf_token()
    _set_csrf_cookie(response, csrf_token)
    return response


def get_current_csrf_token():
    return getattr(g, 'csrf_token', None)


def generate_csrf_token():
    return secrets.token_urlsafe(32)


def verify_csrf():
    csrf_token = _get_csrf_token_from_header()
    csrf_token_from_cookie = _get_csrf_token_from_cookie()
    if not csrf_token:
        raise CSRFValidationError('Missing CSRF token')

    if not csrf_token_from_cookie:
        raise CSRFValidationError('Missing CSRF in session')

    if not csrf_token == csrf_token_from_cookie:
        raise CSRFValidationError('CSRF token does not match')


def _set_csrf_cookie(response, csrf_token):
    max_age = CSRF_COOKIE_MAX_AGE_SECONDS
    response.set_cookie(
        key=CSRF_TOKEN_NAME,
        value=csrf_token,
        domain=CSRF_COOKIE_DOMAIN,
        max_age=max_age,
    )
    return response


def _get_csrf_token_from_header():
    csrf_token = None
    for header_name in CSRF_HEADER_NAMES:
        csrf_token = request.headers.get(header_name)
        if csrf_token:
            break

    return csrf_token


def _get_csrf_token_from_cookie():
    return request.cookies.get('csrf_token')
