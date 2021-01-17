#!/usr/bin/env python

from alvinchow_backend import app
from alvinchow_backend.app import config  # noqa
from alvinchow_backend.db import get_session
from alvinchow_backend.db.models import *  # noqa
from alvinchow_backend.lib.logger import get_logger
from alvinchow_backend.lib.redis import get_redis_connection   # noqa

app.initialize()

logger = get_logger()
session = get_session()
