import pika
import os

QUEUE_NAME = 'mail_queue' or os.environ['MAIL_QUEUE']
RABBIT_HOST = '127.0.0.1' or os.getenv('RABBIT_HOST')


def start():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBIT_HOST
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    return connection, channel
