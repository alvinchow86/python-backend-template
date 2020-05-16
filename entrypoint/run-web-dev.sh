#!/bin/bash
DEVELOP=${DEVELOP:-1}
AUTORELOAD=${AUTORELOAD:-1}
PORT=${PORT:-8000}
FLASK_DEBUGGER=${FLASK_DEBUGGER:-0}

if [ -f /.dockerenv ]; then
  # only do this stuff if running in Docker
  until psql -c "select 1" > /dev/null 2>&1; do
    echo "Waiting for Postgres server to start up..."
    sleep 1
  done

  if [ "$( psql -tAc "SELECT 1 FROM pg_database WHERE datname='alvinchow_service'" )" != '1' ];
  then
    echo "Database does not exist, creating 'alvinchow_service'"
    createdb alvinchow_service
    ./manage.py db reset --migrate
  fi
fi

if [[ $DEVELOP == "1" ]]; then
  FLASK_DEBUGGER=$FLASK_DEBUGGER FLASK_AUTORELOAD=$AUTORELOAD ./manage.py runserver -p ${PORT}
else
  /home/app/entrypoint/run-web.sh
fi
