FROM python:3.10

WORKDIR /opt/app/etl

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH '/opt/app'

COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt
COPY .env .env

RUN apt-get update && apt-get install -y netcat-traditional

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY  .. .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/opt/app/etl/entrypoint.sh"]