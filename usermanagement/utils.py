from django.core.mail import send_mail as sendMail
from django.conf import settings
import json
from io import BytesIO
from django.http import FileResponse


def generate_user_from_email(email):
    return email.replace("@", "")

def generate_email_json(teamName, mailAddress, mailSubject, mailContent, password=None):
    email_json = {
        'teamName': teamName,
        "mailAddress": mailAddress,
        "mailSubject": mailSubject,
        "mailContent": mailContent,
        "password": password
    }
    return email_json

def send_mail(teamName, email, mailSubject, mailContent, password=None):

    subject = mailSubject
    message = mailContent
    if password:
        message += "\n\n Your user is: %s \n Your password is %s" % (generate_user_from_email(email), password)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]   
    sendMail(subject, "", email_from, recipient_list, html_message=message)


def export_teams(adminType):
     # I seriously tried to avoid this bullcrap, but finally because of serializers there was no ducking conditions.

    from .admin import OnlineTeamAdmin, OnsiteTeamAdmin
    from .api.serializers import OnsiteTeamSerializer, OnlineTeamListSerializerWithAuth
    from .models import OnlineTeam, OnsiteTeam

    if adminType is OnlineTeamAdmin:
        team_class = OnlineTeam
        serializer_class = OnlineTeamListSerializerWithAuth
    elif adminType is OnsiteTeamAdmin:
        team_class = OnsiteTeam
        serializer_class = OnsiteTeamSerializer
    
    teams = team_class.objects.all()
    serializer = serializer_class(teams, many=True)
    return serializer.data

# Separator is either comma or a tab character
def json_to_sv_file_response(json_obj, file_name, separator):

    # Keep track of headers in a set
    headers = json_obj[0].keys()

    # You only know what headers were there once you have read all the JSON once.
    # Now we have all the information we need, like what all possible headers are.
    
    sv_str = separator.join(headers) + '\n'
    for record in json_obj:
        currentLine = []
        for header in headers:
            if header in record.keys():
                currentLine.append(record[header])
            else:
                currentLine.append('')
            sv_str += separator.join(currentLine, '\n')
    
    sv_bytes = str.encode(sv_str, encoding='utf-8')
    sv_bytesIO = BytesIO(sv_bytes)
    response = FileResponse(sv_bytesIO)
    response['Content-Disposition'] = 'attachment; filename= %s' %file_name
    return response
