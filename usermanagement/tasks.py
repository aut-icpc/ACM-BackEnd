import django_rq
from usermanagement.apps import UsermanagementConfig as conf
from usermanagement.utils import send_mail, seconds_until_end_of_day
import time

def enqueue_mail(team_instance, subject, content):
    queue = django_rq.get_queue('emails', connection=conf.redis_mail_cursor)
    if team_instance.status == 'FINALIZED':
        queue.enqueue(send_rq_mail, team_instance.get_emails(), subject, content, team_instance.user, team_instance.password)
    else:
        queue.enqueue(send_rq_mail, team_instance.get_emails(), subject, content, None, None)

        

def send_rq_mail(teamName, mailAddresses, mailSubject, mailContent, user=None, password=None):
    r = conf.redis_limit_cursor
    # it returns a byte, so it has to be cast to an integer.
    mails_left = float(r.get('mails_left'))
    
    if mails_left > 0:
        send_mail(mailAddresses, mailSubject, mailContent, user, password)
        time.sleep(conf.delay)
        r.set("mails_left", mails_left - 1)
    else:
        remaining_seconds = seconds_until_end_of_day()
        time.sleep(remaining_seconds)
        send_mail(mailAddresses, mailSubject, mailContent, user, password)
        max_mails = float(r.get("max_mail_limit"))
        r.set("mails_left", max_mails)
