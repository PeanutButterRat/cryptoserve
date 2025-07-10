FROM python:3.11-buster AS builder

RUN pip install poetry==2.1.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without tests --with docs --no-root

FROM python:3.11-slim-buster AS app-runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY src/cryptoserve ./cryptoserve

EXPOSE 5050

ENTRYPOINT ["python", "-m", "cryptoserve.cli"]


FROM builder AS docs

WORKDIR /app

ENV PYTHONPATH=/app

COPY src/cryptoserve ./cryptoserve
COPY docs/ ./docs
COPY tests ./tests

RUN date && ls -ls .

RUN .venv/bin/sphinx-build -b html docs/source docs/build/html


FROM nginx:alpine AS docs-runtime

COPY --from=docs /app/docs/build/html /usr/share/nginx/html

EXPOSE 80
