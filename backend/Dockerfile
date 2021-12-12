FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14

RUN apk --no-cache add \
    build-base \
    curl

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN apk --no-cache add \
    postgresql-dev

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY ./alembic.ini /app/
COPY ./alembic /app/alembic
COPY ./resslab_tools /app/resslab_tools
