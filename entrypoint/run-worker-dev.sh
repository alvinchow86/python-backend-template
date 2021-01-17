#!/bin/bash
DEVELOP=${DEVELOP:-1}
AUTORELOAD=${AUTORELOAD:-1}

if [[ $DEVELOP == "1" ]]; then
  CELERY_COMMAND="celery --app alvinchow_backend.app.worker worker -l info -c1 --without-mingle --without-gossip --without-heartbeat"
  if [[ $AUTORELOAD == "1" ]]; then
      watchmedo auto-restart -d . -p '*.py' --recursive -- $CELERY_COMMAND
    else
      $CELERY_COMMAND
    fi
else
  /home/app/entrypoint/run-worker.sh
fi
