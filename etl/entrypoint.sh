#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "PostgreSQL started"

python3 _elastic_index.py
python3 sqlite_to_postgres/load_data.py
python3 main.py
