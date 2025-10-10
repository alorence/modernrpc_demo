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

RUN --mount=source=package.json,target=package.json \
    --mount=source=pnpm-lock.yaml,target=pnpm-lock.yaml \
    pnpm install --ignore-scripts

RUN --mount=source=package.json,target=package.json \
    --mount=source=pnpm-lock.yaml,target=pnpm-lock.yaml \
    --mount=source=rollup.config.mjs,target=rollup.config.mjs \
    --mount=source=www,target=www \
    --mount=source=main,target=main \
    pnpm run build:prod


FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-base


FROM python:${PYTHON_VERSION}
ARG BUILD_DIR
ARG PROJECT_DIR
ARG DEFAULT_LISTEN_PORT

# gunicorn config: https://docs.gunicorn.org/en/stable/settings.html#bind
# If the PORT environment variable is defined, the default is ['0.0.0.0:$PORT']. Default is ['127.0.0.1:8000'].
ENV PORT=$DEFAULT_LISTEN_PORT
ENV ENVIRONMENT=prod
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN mkdir -p ${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}
EXPOSE 8000

COPY --from=uv-base /uv /uvx /bin/

RUN --mount=type=cache,target=~/.cache/uv \
    --mount=source=pyproject.toml,target=pyproject.toml \
    --mount=source=uv.lock,target=uv.lock \
    uv sync --group=prod --no-group=dev

COPY --parents core/ main/ manage.py ${PROJECT_DIR}

RUN --mount=from=frontend,source=${BUILD_DIR}/dist,target=dist \
     python manage.py collectstatic --no-input

CMD ["gunicorn", "-k", "core.asgi.DjangoUvicornWorker", "-w", "4", "core.asgi:application"]
