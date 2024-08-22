FROM python:3.11-slim-buster AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc git

WORKDIR $PYSETUP_PATH
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip==24.0

RUN pip install -r ./requirements.txt --no-cache

FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./src /app/src