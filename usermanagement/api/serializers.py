from rest_framework import serializers
from django.conf import settings
from django.views.defaults import bad_request
from ..utils import generate_user_from_email
from .utils import createContestants

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
online_team_fields = team_fields + ['country']


class OnsiteContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnsiteContestant
        fields = contestant_fields + ['shirt_size']


class OnlineContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineContestant
        fields = contestant_fields


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country 
        exclude = ('id', )


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
    country = serializers.SlugRelatedField(slug_field='name', queryset=Country.objects.all())

    class Meta:
        model = OnlineTeam
        fields = online_team_fields

    def create(self, validated_data):

        team = createContestants(validated_data, OnlineTeam, OnlineContestant)
        return team

class OnlineTeamListSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = OnlineTeam
        fields = online_team_fields


class OnlineTeamListSerializerWithAuth(OnlineTeamListSerializer):
    user = serializers.SerializerMethodField()
    contestants = OnlineContestantSerializer(many=True)

    class Meta:
        fields = online_team_fields + ['password', 'user']

    def get_user(self, obj):
        user = generate_user_from_email(obj.contestants[0].email)
        return user


class OnsiteTeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnsiteTeam
        exclude = ('id', )

