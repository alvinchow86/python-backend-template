FROM python:3.8.3-alpine3.11

ARG FURY_AUTH

WORKDIR /home/app

RUN mkdir -p /home/app

# Install expensive things
RUN \
  apk add --no-cache bash postgresql-client nginx \
  && apk add --no-cache --virtual native-deps python3-dev g++ linux-headers git \
  && pip install pip==20.1 \
  && apk add --no-cache libstdc++ \
  && pip install pipenv uwsgi \
  && pip install git+https://github.com/Supervisor/supervisor \
  && pip install Cython==0.29.15 grpcio==1.29.0 \
  && apk del native-deps

# Optimization trick to cache pip libraries if not changed
COPY Pipfile Pipfile.lock ./

RUN \
  apk add --no-cache --virtual build-deps libffi-dev g++ \
    postgresql-dev python3-dev \
  && pipenv install --system --dev \
  && apk del build-deps

# Copy rest of files
COPY . /home/app

RUN mkdir /etc/supervisor.d && ln -s /home/app/infra/supervisord.conf /etc/ && \
    mkdir /var/log/supervisor && \
    rm /etc/nginx/nginx.conf && rm /etc/nginx/conf.d/default.conf && \
    ln -s /home/app/infra/nginx.conf /etc/nginx/ && \
    addgroup -S web && adduser -S web -G web

RUN pip install -e .

CMD "/home/app/entrypoint/run-web.sh"
