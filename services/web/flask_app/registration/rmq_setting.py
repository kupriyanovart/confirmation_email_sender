import os

import pika

MAIL_QUEUE_NAME = 'mail_validator'


class RabbitMQMailPublisher:
    def __init__(self):
        credentials = pika.PlainCredentials(
            os.environ.get("RABBITMQ_CONNECTION_USERNAME"),
            os.environ.get("RABBITMQ_CONNECTION_PASSWORD"),
        )
        parameters = pika.ConnectionParameters(os.environ.get("RABBITMQ_CONNECTION_HOST"),
                                               os.environ.get("RABBITMQ_CONNECTION_PORT"),
                                               '/',
                                               credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue=MAIL_QUEUE_NAME)
        self.queue_name = MAIL_QUEUE_NAME
        self.channel = channel

    def publish(self, body):
        self.channel.basic_publish(exchange="", routing_key=self.queue_name, body=body)

