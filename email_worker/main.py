import pika, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBIT_MQ_SERVER']))
    channel = connection.channel()


if __name__ == '__main__':
    main()
