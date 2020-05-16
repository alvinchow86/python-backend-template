#!/usr/bin/env python

from alvinchow_service import app
from alvinchow_service.app import config  # noqa
from alvinchow_service.db import get_session
from alvinchow_service.db.models import *  # noqa
from alvinchow_service.lib.logger import get_logger
from alvinchow_service.lib.redis import get_redis_connection   # noqa

app.initialize()

logger = get_logger()
session = get_session()
