FROM python:3.8.18-slim-bullseye

EXPOSE 80

ENV POETRY_VERSION=1.6.0 \
    POETRY_HOME=/opt/poetry \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=0 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache


# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN pip install --no-cache-dir poetry==1.6.0
RUN apt-get update && apt-get install -y supervisor && apt-get clean


WORKDIR /app

RUN touch README.md

COPY pyproject.toml poetry.lock ./

COPY src ./src
RUN poetry install
COPY models ./models

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "80"]