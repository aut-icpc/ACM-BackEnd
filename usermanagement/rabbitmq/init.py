import pika
QUEUE_NAME = 'mail_queue'

def start():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    return connection, channel


def close_connection(connection):
    connection.close()
