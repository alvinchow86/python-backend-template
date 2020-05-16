#!/bin/bash
ln -sf /home/app/infra/supervisor-worker.ini /etc/supervisor.d/ &&
exec supervisord -n -c /etc/supervisord.conf
