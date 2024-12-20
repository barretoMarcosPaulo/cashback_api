FROM python:3.11-slim

ENV POETRY_VERSION=1.7.2
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY . .

EXPOSE 8000

