#!/bin/bash
ln -sf /home/app/infra/supervisor-grpc.ini /etc/supervisor.d/ &&
exec supervisord -n -c /etc/supervisord.conf
