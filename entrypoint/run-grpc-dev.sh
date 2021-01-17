#!/bin/bash
DEVELOP=${DEVELOP:-1}
AUTORELOAD=${AUTORELOAD:-0}
GRPC_PORT=${GRPC_PORT:-50051}

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
  if [[ $AUTORELOAD == "1" ]]; then
     echo "Running gRPC server with autoreload"
     watchmedo auto-restart -d . -p'*.py' --recursive -- ./manage.py rungrpcserver
  else
    ./manage.py rungrpcserver
  fi
else
  /home/app/entrypoint/run-grpc.sh
fi
