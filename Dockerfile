# syntax=docker.io/docker/dockerfile:1.7-labs
ARG PYTHON_VERSION=3.14-alpine
ARG NODE_VERSION=24-alpine
ARG UV_VERSION=0.9.1

ARG DEFAULT_LISTEN_PORT=8099
ARG BUILD_DIR=/build
ARG PROJECT_DIR=/app


FROM node:${NODE_VERSION} AS frontend
ARG BUILD_DIR

WORKDIR ${BUILD_DIR}
RUN corepack enable

COPY package.json pnpm-lock.yaml rollup.config.mjs ${BUILD_DIR}
RUN pnpm install --ignore-scripts

COPY --parents www/ main/ ${BUILD_DIR}
RUN pnpm run build:prod


FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-base


FROM python:${PYTHON_VERSION} AS python-base
ARG PROJECT_DIR

ENV ENVIRONMENT=prod
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN mkdir -p ${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}

COPY --from=uv-base /uv /uvx /bin/

RUN --mount=type=cache,target=~/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --group=prod --no-group=dev

COPY --parents core/ main/ manage.py ${PROJECT_DIR}


FROM python-base AS collectstatic
ARG BUILD_DIR
ARG PROJECT_DIR

COPY --from=frontend ${BUILD_DIR}/dist ${PROJECT_DIR}/dist
RUN python manage.py collectstatic --no-input


FROM python-base
ARG PROJECT_DIR
ARG DEFAULT_LISTEN_PORT

# gunicorn config: https://docs.gunicorn.org/en/stable/settings.html#bind
# If the PORT environment variable is defined, the default is ['0.0.0.0:$PORT']. Default is ['127.0.0.1:8000'].
ENV PORT=$DEFAULT_LISTEN_PORT

# Extract currently configured STATIC_ROOT from Django settings and store it in DJANGO_STATIC_ROOT envvar
RUN export DJANGO_STATIC_ROOT=$(python manage.py shell -c 'from django.conf import *; print(settings.STATIC_ROOT)')
COPY --from=collectstatic ${DJANGO_STATIC_ROOT} ${DJANGO_STATIC_ROOT}

EXPOSE 8000

CMD ["gunicorn", "-k", "core.asgi.DjangoUvicornWorker", "-w", "4", "core.asgi:application"]
