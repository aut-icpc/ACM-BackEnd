from django.core.exceptions import SuspiciousOperation
from django.db.models import Q
from django.conf import settings
from rest_framework.exceptions import APIException
from usermanagement.models import OnlineTeam

import json, urllib

class TemporarilyUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

def check_uniqueness(contestant_list):
    meta = contestant_list[0]._meta
    model = meta.model
    model_fields = meta.get_fields()

    unique_field_names = [ field.name for field in model_fields if field.unique ]
    eachother_check_list = {name: [] for name in unique_field_names}
    for contestant in contestant_list:
        q = Q()
        for field_name in unique_field_names:
            # Check if equivalent fields are present in the database
            try:
                attribute = getattr(contestant, field_name)
                if attribute:
                    query_dict = {field_name: attribute}
                    q |= Q(**query_dict)

                    # Check if contestants are unique from eachother
                    attribute_list = eachother_check_list[field_name]
                    if str(attribute) in attribute_list:
                        raise SuspiciousOperation("Similar contestants in one team!")
                    else:
                        eachother_check_list[field_name].append(str(attribute))
            except AttributeError:
                print("Contestant has no attribute %s" % field_name)
            

        if len(model.objects.filter(q)) != 0:
            raise SuspiciousOperation("Similar contestant already present in the database!")


def validate_uniqueness(validated_data, contestantType, team, contestants_data, main_contestant_data):
    main_contestant = contestantType(team=team, **main_contestant_data)
    main_contestant.is_primary = True
    contestants = [main_contestant,]
    for contestant_data in contestants_data[1:]:
        contestant = contestantType(team=team, **contestant_data)
        contestants.append(contestant)
        
    check_uniqueness(contestants)
    return contestants

def create_contestants(validated_data, TeamType, ContestantType):
    
    contestants_data = validated_data.pop('contestants')
    main_contestant_data = contestants_data[0]
    team = TeamType(**validated_data)
    team.email = main_contestant_data['email']
    team.emails = [data['email'] for data in contestants_data]

    contestants = validate_uniqueness(validated_data, ContestantType, team, contestants_data, main_contestant_data)
    try:
        team.sendNewMail = True
        team.save()
    except:
        raise
    # contestants = validate_uniqueness(validated_data, ContestantType, team, contestants_data, main_contestant_data)
    for contestant in contestants:
        contestant.team = team
        contestant.save()
    return team


def validate_recaptcha(request):
    recaptcha_response = request.data['recaptcha']
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req  =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    #TODO: Find out what was wrong with recaptcha validation.
    print(result)
    if result['success']:
        return True
    return False


def validate_contestants(contestant_serializer, contestant_list):
    if len(contestant_list) == 3:
        result = True
        for contestant in contestant_list:
            serializer = contestant_serializer(data=contestant)
            result &= serializer.is_valid()
        return result
    return False
