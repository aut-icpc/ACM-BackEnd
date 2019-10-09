import pika
import os

QUEUE_NAME = os.environ['MAIL_QUEUE']


def start():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBIT_HOST")
            # host='localhost'
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    return connection, channel
