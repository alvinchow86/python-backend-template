#!/bin/bash
ln -sf /home/app/infra/supervisor-web.ini /etc/supervisor.d/ &&
ln -sf /home/app/infra/nginx-web.conf /etc/nginx/conf.d &&
exec supervisord -n -c /etc/supervisord.conf
