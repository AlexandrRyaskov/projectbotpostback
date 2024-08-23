FROM python:3.11-slim-buster


COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt --no-cache

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./src /app/src
COPY ./pyproject.toml /app
RUN pip install --editable .