FROM python:3.10.4

WORKDIR opt/app/tests

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/opt/app'

COPY functional/requirements.txt requirements.txt
COPY functional/.env .env


RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY .. .