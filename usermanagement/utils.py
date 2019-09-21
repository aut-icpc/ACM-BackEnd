from django.core.mail import send_mail as sendMail
from django.conf import settings


def send_mail(OnsiteContestantTeamName, OnsiteContestantEmail, MailMessageSubject, MailMessageContent):

    subject = MailMessageSubject
    message = MailMessageContent
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [OnsiteContestantEmail, ]   
    sendMail(subject, message, email_from, recipient_list)
