from django.core.mail import send_mail as sendMail
from django.conf import settings
from rest_framework.renderers import JSONRenderer
import json




def send_mail(ContestantTeamName, ContestantEmail, MailMessageSubject, MailMessageContent):

    subject = MailMessageSubject
    message = MailMessageContent
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [ContestantEmail, ]   
    sendMail(subject, message, email_from, recipient_list)


def export_teams(adminType):
     # I seriously tried to avoid this bullcrap, but finally because of serializers there was no ducking conditions.

    from .admin import OnlineTeamAdmin, OnsiteTeamAdmin
    from .api.serializers import OnlineTeamListSerializer, OnsiteTeamListSerializer
    from .models import OnlineTeam, OnsiteTeam
    if adminType is OnlineTeamAdmin:
        team_class = OnlineTeam
        serializer_class = OnlineTeamListSerializer
    elif adminType is OnsiteTeamAdmin:
        team_class = OnsiteTeam
        serializer_class = OnsiteTeamListSerializer
    teams = team_class.objects.all()
    serializer = serializer_class(teams, many=True)
    # content = JSONRenderer().render(serializer.data)
    return serializer.data


def write_json_to_csv_file(json_obj, file_name):
    # Because somehow rest_framework returns the orderedDict inside of a list, why?!

    # Keep track of headers in a set
    headers = json_obj[0].keys()

    # You only know what headers were there once you have read all the JSON once.
    # Now we have all the information we need, like what all possible headers are.

    with open(file_name, 'w') as outfile:
    # write headers to the file in order
        outfile.write(",".join(headers) + '\n')

        for record in json_obj:
            # write each record based on available fields
            curLine = []
            for header in headers:
                if header in record.keys():
                    curLine.append(record[header])
                else:
                    curLine.append('')
            outfile.write(",".join(curLine) + '\n')
