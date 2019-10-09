import os, datetime, time, json
import pika, yagmail
from rabbit_utils import start, seconds_until_end_of_day, mail_sender, QUEUE_NAME
class state:

    MAILING_LIMIT = 90
    mails_left = MAILING_LIMIT
        
    

def send_email(ch, method, properties, body):
    email_dict = json.loads(body)
    if state.mails_left > 1:
        try:
            mail_sender.send_mail(**email_dict)
            state.mails_left -= 1
        except Exception as ex:
            print(ex)
    else:
        waiting_seconds = seconds_until_end_of_day()
        time.sleep(waiting_seconds)
        mail_sender.send_mail(**email_dict)
        state.mails_left = state.MAILING_LIMIT
    ch.basic_ack(
        delivery_tag = method.delivery_tag
    )


def close_connection(connection):
    connection.close()


def main():

    connection, channel = start()
    channel.basic_consume(
        queue = QUEUE_NAME,
        on_message_callback = send_email,
        auto_ack = False
    )
    


if __name__ == '__main__':
    main()
