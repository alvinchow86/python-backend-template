from datetime import timedelta
from easydict import EasyDict
import json
import secrets
import time

from alvinchow.lib.dates import utcnow
from alvinchow_backend.lib.redis import get_session_redis_connection
from alvinchow_backend.service.authentication.constants import DEFAULT_SESSION_EXPIRATION_SECONDS

SESSION_TOKEN_BYTES = 64


def _get_current_timestamp():
    return int(round(time.time()))


def create_session_token():
    return secrets.token_urlsafe(SESSION_TOKEN_BYTES)


def get_session_token_redis_key(token):
    # Add short prefix to group session
    return 'session:{}'.format(token)


def _get_expiration_params(expiration_seconds=None):
    expiration_seconds = expiration_seconds or DEFAULT_SESSION_EXPIRATION_SECONDS

    now = utcnow()
    expires_at = now + timedelta(seconds=expiration_seconds)
    expiration_timestamp = int(round(expires_at.timestamp()))

    return EasyDict(
        datetime=now,
        seconds=expiration_seconds,
        timestamp=expiration_timestamp,
    )


def create_session(data=None, expiration_seconds=None):
    conn = get_session_redis_connection()

    data = data or {}

    session_token = create_session_token()
    session_redis_key = get_session_token_redis_key(session_token)

    expiration_params = _get_expiration_params(expiration_seconds=expiration_seconds)

    data.update(
        _created_at=_get_current_timestamp(),
        # _expires_at=expiration_params.timestamp
    )

    serialized_data = json.dumps(data).encode('utf8')
    conn.set(session_redis_key, serialized_data, ex=expiration_params.seconds)

    return EasyDict(
        token=session_token,
        expires_at=expiration_params.datetime,
    )


def write_session(session_token, data, expiration_seconds=None):
    conn = get_session_redis_connection()
    session_redis_key = get_session_token_redis_key(session_token)

    expiration_params = _get_expiration_params(expiration_seconds=expiration_seconds)

    serialized_data = json.dumps(data)
    conn.set(session_redis_key, serialized_data, ex=expiration_params.seconds)


def get_session_data(session_token):
    conn = get_session_redis_connection()

    session_redis_key = get_session_token_redis_key(session_token)

    raw_data = conn.get(session_redis_key)
    if raw_data is None:
        return None

    data = json.loads(raw_data.decode('utf8'))
    return data


def extend_session(session_token, expiration_seconds=None):
    conn = get_session_redis_connection()
    session_redis_key = get_session_token_redis_key(session_token)
    expiration_params = _get_expiration_params(expiration_seconds=expiration_seconds)

    pipe = conn.pipeline()
    conn.expire(session_redis_key, expiration_params.seconds)
    pipe.execute()


def delete_session(session_token):
    conn = get_session_redis_connection()
    key = get_session_token_redis_key(session_token)

    conn.delete(key)


def does_session_exist(session_token):
    conn = get_session_redis_connection()
    key = get_session_token_redis_key(session_token)
    return conn.exists(key)
