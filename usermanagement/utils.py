from django.core.mail import send_mail as sendMail


def send_mail(OnsiteContestantTeamName, OnsiteContestantEmail, MailMessage=""):

    subject = MailMessage
    message = 'ali nazari ye chizi bego'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [OnsiteContestantEmail, ]   
    sendMail(subject, message, email_from, recipient_list)
