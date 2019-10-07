import pika, json
from . import startup

class Sender:
    def __init__(self):
        self.connection, self.channel = startup.start()

    def publish_mail(self, email_dict):
        self.channel.basic_publish(
            exchange = '',
            routing_key = startup.QUEUE_NAME,
            body = json.dumps(email_dict),
            properties= pika.BasicProperties(
                delivery_mode=2
            )
        )
