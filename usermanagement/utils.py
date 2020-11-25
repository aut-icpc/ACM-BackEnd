from django.core.mail import send_mail as django_send_mail
from django.conf import settings
import datetime
from io import BytesIO
from django.http import FileResponse


def seconds_until_end_of_day(dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    return ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)

def send_mail(recipients, subject, content, user=None, password=None):

    message = content
    if password:
        message += "\n\n Your user is: %s \n Your password is %s" % (user, password)
    # email_from = settings.EMAIL_FROM
    email_from = "\"{}\" <{}>".format(settings.EMAIL_FROM, settings.EMAIL_HOST_USER)
    # recipient_list = [email, ]   
    django_send_mail(subject, "", email_from, recipients, html_message=message)


def export_teams(adminType, is_finalized):
     # I seriously tried to avoid this bullcrap, but because of serializers there was no ducking conditions.

    from .admin import OnlineTeamAdmin, OnsiteTeamAdmin
    from .api.serializers import OnsiteTeamGenerateSerializer, OnlineTeamGenerateSerializer
    from .models import OnlineTeam, OnsiteTeam

    if adminType is OnlineTeamAdmin:
        team_class = OnlineTeam
        serializer_class = OnlineTeamGenerateSerializer
    elif adminType is OnsiteTeamAdmin:
        team_class = OnsiteTeam
        serializer_class = OnsiteTeamGenerateSerializer
    if is_finalized:
        teams = team_class.objects.filter(status='FINALIZED')
    else:
        teams = team_class.objects.all()
    serializer = serializer_class(teams, many=True)

    return serializer.data

def export_contestants(adminType, is_finalized):
    from .admin import OnlineTeamAdmin, OnsiteTeamAdmin
    from .api.serializers import OnsiteContestantGenerateSerializer, OnlineContestantGenerateSerializer
    from .models import OnsiteContestant, OnlineContestant

    if adminType is OnsiteTeamAdmin:
        serializer_class = OnsiteContestantGenerateSerializer
        contestant_class = OnsiteContestant
        team_class = "onsiteteam"
    elif adminType is OnlineTeamAdmin:
        serializer_class = OnlineContestantGenerateSerializer
        contestant_class = OnlineContestant
        team_class = "onlineteam"

    if is_finalized:
        team_ids = []
        contestants_all = contestant_class.objects.all()
        for contestant in contestants_all:
            team_ptr = getattr(contestant.team, team_class)
            if team_ptr.status == 'FINALIZED':
                team_ids.append(team_ptr.id)
        contestants = contestant_class.objects.filter(team__id__in=team_ids).order_by('team__name')
    else:
        contestants = contestant_class.objects.order_by('team__name')

    serializer = serializer_class(contestants, many=True)
    return serializer.data


def create_sv_response(sv_str, file_name):
    sv_bytes = str.encode(sv_str, encoding='utf-8')
    sv_bytesIO = BytesIO(sv_bytes)
    response = FileResponse(sv_bytesIO)
    response['Content-Disposition'] = 'attachment; filename= %s' %file_name
    return response


# Separator is either comma or a tab character

def generate_sv_str(headers, separator):
    headers = [str(header) if header else "PLACEHOLDER" for header in headers]
    return separator.join(headers) + '\n'


def generate_current_line(headers, record, separator, judge=None, judge_type=None):
    headers = headers.copy()
    if judge:
        if judge_type == 'TEAMS':
            # The nested cast is there to remove the zeros and leave the number intact.
            try:
                team_number = str(int(record['user'].split('-')[1]))
            except:
                from random import randint
                team_number = randint(0, 200)
            # the 3 is probably #contestants
            currentLine = [team_number, '\t', '3']
        else:
            currentLine = ['team']
    else:
        currentLine = []
    for header in headers:
        if header in record.keys():
            currentLine.append(record[header])
        else:
            currentLine.append('')

    if judge:
        if judge_type == 'TEAMS':
            abbr = ''.join(w[0].upper() for w in record['institution'].split())
            currentLine.append(abbr[:3])
            if 'country' not in headers:
                currentLine.append('IRN')
    add_str = generate_sv_str(currentLine, separator)
    return add_str


def team_json_to_sv_file_response(json_obj, file_name, separator, judge=None, judge_type=None):

     # Keep track of headers in a set
    headers = list(json_obj[0].keys())

    # You only know what headers were there once you have read all the JSON once.
    # Now we have all the information we need, like what all possible headers are.
    if judge:
        sv_str = judge_type.lower() + separator + '1' + '\n'
        if judge_type == 'TEAMS':
            headers.remove('user')
            headers.remove('password')
        else:
            headers.remove('institution')
            try:
                headers.remove('country')
            except:
                pass
    else:
        sv_str = generate_sv_str(headers, separator)

    for record in json_obj:
        sv_str += generate_current_line(headers, record, separator, judge, judge_type)
    
    return create_sv_response(sv_str, file_name)

