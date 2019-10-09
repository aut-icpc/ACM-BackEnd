import os, datetime
import pika, yagmail

def generate_user_from_email(email):
    return ""


def seconds_until_end_of_day(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    return ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)
    
QUEUE_NAME = os.environ['MAIL_QUEUE']

def start():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.environ['RABBIT_HOST']
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    return connection, channel

class MailSender:
    def __init__(self):
        user = os.environ['EMAIL_HOST_USER']
        password = os.environ['EMAIL_HOST_PASSWORD']
        self.yag = yagmail.SMTP(user, password, port=587)

    def send_mail(self, teamName, mailAddress, mailSubject, mailContent, password=None):
        if password:
            mailContent += "\n Your user is: %s \n Your password is %s" % (generate_user_from_email(mailAddress), password)

        self.yag.send(
            to=mailContent,
            subject=mailSubject,
            contents=mailContent
        )
        
mail_sender = MailSender()