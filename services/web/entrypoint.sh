#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Waiting for Rabbit..."

while ! nc -z rabbitmq 5672; do
  sleep 1
done

echo "Rabbit started"

python manage.py create_db

exec "$@"