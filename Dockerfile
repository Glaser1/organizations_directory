FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV \
    POETRY_VERSION=2.0.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN poetry install --only=main --no-interaction

CMD ["python3", "organizations_directory/main.py"]
