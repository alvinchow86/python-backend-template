from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict

from alvinchow_backend.app import config
from alvinchow_backend.service.authentication.session import (
    create_session, write_session, delete_session, get_session_data, extend_session,
    DEFAULT_SESSION_EXPIRATION_SECONDS
)

SESSION_COOKIE_NAME = config.SESSION_COOKIE_NAME
SESSION_COOKIE_SECURE = config.SESSION_COOKIE_SECURE


class RedisSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, session_id=None, permanent=True):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.session_id = session_id
        if permanent:
            self.permanent = permanent
        self.modified = False


class RedisSessionInterface(SessionInterface):
    def __init__(self, session_cookie_domain=None, session_expiration_seconds=None, *args, **kwargs):
        self.session_cookie_domain = session_cookie_domain
        self.session_expiration_seconds = session_expiration_seconds or DEFAULT_SESSION_EXPIRATION_SECONDS
        super().__init__(*args, **kwargs)

    # borrowed from https://github.com/fengsp/flask-session/blob/master/flask_session/sessions.py
    def open_session(self, app, request):
        session_id = request.cookies.get(SESSION_COOKIE_NAME)

        if not session_id:
            # Create new session + cookie
            session_info = create_session(expiration_seconds=self.session_expiration_seconds)
            session_obj = RedisSession(
                session_id=session_info.token
            )
            return session_obj

        # Read existing session if exists
        session_data = get_session_data(session_id)
        if session_data:
            session_obj = RedisSession(
                session_data,
                session_id=session_id,
            )
            return session_obj

        # No session, return blank one.. (cookie exists but session expired on backend)?? TODO this
        return RedisSession(
            session_id=session_id
        )

    def save_session(self, app, session, response):
        path = self.get_cookie_path(app)
        expires = self.session_expiration_seconds

        session_id = session.session_id

        if not session:
            if session.modified:
                delete_session(session.session_id)
                response.delete_cookie(
                    SESSION_COOKIE_NAME,
                    domain=self.session_cookie_domain,
                    path=path
                )
            return

        data = dict(session)
        if session.modified:
            write_session(session_id, data, expiration_seconds=self.session_expiration_seconds)
        else:
            extend_session(session_id, expiration_seconds=self.session_expiration_seconds)

        response.set_cookie(
            SESSION_COOKIE_NAME,
            session_id,
            max_age=expires,
            httponly=True,
            domain=self.session_cookie_domain,
            path=path,
            secure=SESSION_COOKIE_SECURE,
        )
