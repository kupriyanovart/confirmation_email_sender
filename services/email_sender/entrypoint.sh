#!/bin/sh
echo "Waiting for Rabbit..."

while ! nc -z rabbitmq 5672; do
  sleep 1
done

echo "Rabbit started"

exec "$@"