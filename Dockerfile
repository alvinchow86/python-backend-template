FROM python:3.9.1-slim-buster

ARG FURY_AUTH

WORKDIR /home/app

RUN mkdir -p /home/app

# Install expensive things
# Installing postgresql-client-12 needs extra step (https://www.postgresql.org/download/linux/debian/)
RUN \
  BUILD_DEPS='g++ python3-dev git gnupg' \
  && apt-get update \
  && apt-get install -y nginx wget less git \
  && apt-get install -y --no-install-recommends $BUILD_DEPS \
  && pip install pipenv uwsgi \
  && pip install git+https://github.com/Supervisor/supervisor \
  && echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
  && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
  && apt-get update \
  && apt-get install -y postgresql-client-12 \
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

RUN pip install -e alvin-python-lib -e alvin-grpc-py -e .

CMD "/home/app/entrypoint/run-web.sh"
