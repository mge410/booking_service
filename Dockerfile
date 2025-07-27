FROM python:3.13-slim as builder

RUN pip install poetry
WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

FROM python:3.13-slim

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY --chown=appuser:appuser . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/appuser/.local/bin:${PATH}"

USER appuser

EXPOSE 8000

WORKDIR /app/booking_service
