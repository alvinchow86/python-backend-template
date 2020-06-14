FROM python:3.8.3-slim-buster

ARG FURY_AUTH

WORKDIR /home/app

RUN mkdir -p /home/app

# Install expensive things
RUN \
  BUILD_DEPS='g++ python3-dev git' \
  && apt-get update \
  && apt-get install -y postgresql-client nginx \
  && apt-get install -y --no-install-recommends $BUILD_DEPS \
  && pip install pipenv uwsgi \
  && pip install git+https://github.com/Supervisor/supervisor \
  && pip install Cython==0.29.15 grpcio==1.29.0 \
  && apt-get purge --autoremove -y $BUILD_DEPS \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Optimization trick to cache pip libraries if not changed
COPY Pipfile Pipfile.lock ./

RUN \
  BUILD_DEPS='g++ python3-dev libffi-dev libpq-dev' \
  && apt-get update \
  && apt-get install -y --no-install-recommends $BUILD_DEPS \
  && pipenv install --system --dev \
  && apt-get purge --autoremove -y $BUILD_DEPS \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Copy rest of files
COPY . /home/app

RUN mkdir /etc/supervisor.d && ln -s /home/app/infra/supervisord.conf /etc/ && \
    mkdir /var/log/supervisor && \
    rm /etc/nginx/nginx.conf && \
    ln -s /home/app/infra/nginx.conf /etc/nginx/ && \
    groupadd web && useradd web -g web

RUN pip install -e .

CMD "/home/app/entrypoint/run-web.sh"
