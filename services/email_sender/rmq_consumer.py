import json
import os

import pika
import logging
from flask import Flask
from flask_mail import Mail, Message

queue_name = 'mail_validator'

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)

worker = 'Consumer: '

app = Flask(__name__)

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
# Если логин и пароль гугл не принимает -> https://stackoverflow.com/a/27515883/17482225
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")  # FILL ME
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")  # FILL ME
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")  # FILL ME
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS") in ("True",)
app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL") in ("True",)
mail = Mail(app)


def callback(ch, method, properties, body):
    LOG.info(worker + "received:\t%s" % body)
    body = json.loads(body)
    email = body["email"]
    token = body["token"]
    url = body["base_url"]

    with app.app_context():
        msg = Message(f"Confirm Your Registration at {url}",
                      recipients=[email])
        msg.html = f"Follow <a href=\"{url}confirm?token=" + token + "\">this</a> " \
                                                                     "link to confirm your email."
        mail.send(msg)


if __name__ == '__main__':
    credentials = pika.PlainCredentials(
        os.environ.get("RABBITMQ_CONNECTION_USERNAME"),
        os.environ.get("RABBITMQ_CONNECTION_PASSWORD"),
    )
    parameters = pika.ConnectionParameters(os.environ.get("RABBITMQ_CONNECTION_HOST"),
                                           5672,
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_consume(on_message_callback=callback,
                          queue=queue_name,
                          auto_ack=True)

    LOG.info(worker + 'Waiting for messages. To exit press Ctrl+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        LOG.info(worker + 'closing connection...')
        connection.close()
