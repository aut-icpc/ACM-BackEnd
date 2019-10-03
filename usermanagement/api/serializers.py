from rest_framework import serializers
from django.conf import settings
from usermanagement.models import (
    Country,
    OnlineTeam,
    OnsiteTeam,
    OnlineContestant,
    OnsiteContestant,
    Team,
    MailMessage
)

contestant_fields = ['first_name', 'last_name', 'gender', 'edu_level', 'student_number', 'email', 'phone_number']
team_fields = ['name', 'status', 'institution', 'contestants']


class OnsiteContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnsiteContestant
        fields = contestant_fields


class OnlineContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineContestant
        fields = contestant_fields


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country 
        # fields = '__all__'
        exclude = ('id', )


def createContestants(validated_data, TeamType, ContestantType):
    contestants_data = validated_data.pop('contestants')
    email = contestants_data[0]['email']
    # team = TeamType.objects.create(**validated_data)
    team = TeamType(**validated_data)
    team.email = email
    team.save()
    for contestant_data in contestants_data:
        ContestantType.objects.create(team=team, **contestant_data)
    return team


class OnsiteTeamSerializer(serializers.ModelSerializer):
    contestants = OnsiteContestantSerializer(many=True)

    class Meta:
        model = OnsiteTeam
        fields = team_fields

    def create(self, validated_data):
        team = createContestants(validated_data, OnsiteTeam, OnsiteContestant)
        return team


class OnlineTeamSerializer(serializers.ModelSerializer):
    contestants = OnlineContestantSerializer(many=True)

    class Meta:
        model = OnlineTeam
        fields = team_fields + ['country']

    def create(self, validated_data):
        team = createContestants(validated_data, OnlineTeam, OnlineContestant)
        
        return team


class OnlineTeamListSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = OnlineTeam
        fields = ['name', 'institution', 'status', 'country']


class OnsiteTeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnsiteTeam
        exclude = ('id', )
        # fields = '__all__'
