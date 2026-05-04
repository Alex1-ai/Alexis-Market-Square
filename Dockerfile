ARG PYTHON_VERSION=3.10-slim-bullseye  # ← changed from buster to bullseye

ARG DEBIAN_FRONTEND=noninteractive

ARG PORT=8000

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app

WORKDIR /app

# install the linux packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    cron \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /app



EXPOSE ${PORT}

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
