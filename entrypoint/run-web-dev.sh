#!/bin/bash
DEVELOP=${DEVELOP:-1}
AUTORELOAD=${AUTORELOAD:-1}
PORT=${PORT:-5000}
FLASK_DEBUGGER=${FLASK_DEBUGGER:-0}
FLASK_SSL=${SSL:-0}

if [ -f /.dockerenv ]; then
  # only do this stuff if running in Docker
  until psql -c "select 1" > /dev/null 2>&1; do
    echo "Waiting for Postgres server to start up..."
    sleep 1
  done

  if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='alvinchow_backend'" )" != '1' ];
  then
    echo "Database does not exist, creating 'alvinchow_backend'"
    createdb alvinchow_backend
    ./manage.py db reset --migrate
  fi
fi

if [[ $DEVELOP == "1" ]]; then
  while true; do
    echo "Starting development server (autoreload=$AUTORELOAD)"
    if [[ $AUTORELOAD == "1" ]]; then
      echo "Running Flask with watchdog"
      FLASK_DEBUGGER=$FLASK_DEBUGGER FLASK_SSL=$FLASK_SSL watchmedo auto-restart -d . -p'*.py' --recursive -- ./manage.py runserver -p ${PORT}
    else
      FLASK_DEBUGGER=$FLASK_DEBUGGER FLASK_SSL=$FLASK_SSL ./manage.py runserver -p ${PORT}
    fi
    #FLASK_DEBUGGER=$FLASK_DEBUGGER FLASK_AUTORELOAD=$AUTORELOAD FLASK_SSL=$FLASK_SSL ./manage.py runserver -p ${PORT}
    echo "Server exited with code $?.. restarting in a few seconds..."
    sleep 2
  done
else
  /home/app/entrypoint/run-web.sh
fi
