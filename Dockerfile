ARG PYTHON_VERSION=3.13-alpine
ARG NODE_VERSION=24-alpine
ARG UV_VERSION=0.8.23

ARG DEFAULT_LISTEN_PORT=8099
ARG BUILD_DIR=/build
ARG PROJECT_DIR=/app


FROM node:${NODE_VERSION} AS frontend
ARG BUILD_DIR

WORKDIR ${BUILD_DIR}
RUN corepack enable
COPY package.json pnpm-lock.yaml rollup.config.mjs ${BUILD_DIR}
COPY www ${BUILD_DIR}/www
RUN ls -al www/
RUN pnpm install --ignore-scripts && pnpm run build:prod


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

COPY . ${PROJECT_DIR}


FROM python-base AS collectstatic
ARG BUILD_DIR
ARG PROJECT_DIR

COPY --from=frontend ${BUILD_DIR}/dist ${PROJECT_DIR}/dist
RUN python manage.py collectstatic --no-input


FROM python-base
ARG PROJECT_DIR
ARG DEFAULT_LISTEN_PORT

# Must be consistent with settings.STATIC_ROOT
# TODO: load this from env var
ENV DJANGO_STATIC_ROOT=${PROJECT_DIR}/static
# gunicorn config: https://docs.gunicorn.org/en/stable/settings.html#bind
# If the PORT environment variable is defined, the default is ['0.0.0.0:$PORT']. Default is ['127.0.0.1:8000'].
ENV PORT=$DEFAULT_LISTEN_PORT

COPY --from=collectstatic ${DJANGO_STATIC_ROOT} ${DJANGO_STATIC_ROOT}

EXPOSE 8000

CMD ["gunicorn", "-k", "core.asgi.DjangoUvicornWorker", "core.asgi:application"]
