import pika, json
import init

connection, channel = init.start()

def publish_mail(email_dict):
    channel.basic_publish(
        exchange = '',
        routing_key = init.QUEUE_NAME,
        body = json.dumps(email_dict),
        properties= pika.BasicProperties(
            delivery_mode=2
        )
    )

