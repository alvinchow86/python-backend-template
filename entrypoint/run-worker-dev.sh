#!/bin/bash
DEVELOP=${DEVELOP:-1}

if [[ $DEVELOP == "1" ]]; then
  celery worker -A alvinchow_service.app.worker -l info -c1 --without-mingle --without-gossip --without-heartbeat
else
  /home/app/entrypoint/run-worker.sh
fi
