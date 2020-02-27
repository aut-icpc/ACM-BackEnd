from rest_framework import serializers
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from ..utils import generate_user_from_email
from .utils import createContestants, validate_contestants

from usermanagement.models import (
    Country,
    OnlineTeam,
    OnsiteTeam,
    OnlineContestant,
    OnsiteContestant,
    Team,
    MailMessage
)

contestant_fields = ['first_name', 'last_name', 'gender', 'edu_level', 'student_number', 'email']
onsite_contestant_fields = contestant_fields + ['phone_number', 'shirt_size']
team_fields = ['name', 'institution', 'contestants'] 
online_fields = ['country', ]
online_team_fields = team_fields + online_fields
create_onsite_team_fields = team_fields + ['recaptcha', ]
create_online_team_fields = create_onsite_team_fields + online_fields
generate_team_fields = ['name', 'institution']
generate_online_team_fields = generate_team_fields + online_fields
generate_contestant_fields = ['team', 'institution']


class OnsiteContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnsiteContestant
        fields = onsite_contestant_fields


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
    recaptcha = serializers.ReadOnlyField()

    class Meta:
        model = OnsiteTeam
        fields = create_onsite_team_fields

    def create(self, validated_data):
        team = createContestants(validated_data, OnsiteTeam, OnsiteContestant)
        return team

    def validate(self, data):
        if validate_contestants(OnsiteContestantSerializer, data['contestants']):
            super_val = super(OnsiteTeamSerializer, self).validate(data)
            return super_val
        raise SuspiciousOperation("Invalid contestants!")


class OnlineTeamSerializer(serializers.ModelSerializer):
    contestants = OnlineContestantSerializer(many=True)
    country = serializers.SlugRelatedField(slug_field='name', queryset=Country.objects.all())
    recaptcha = serializers.ReadOnlyField()

    class Meta:
        model = OnlineTeam
        fields = create_online_team_fields
        # String

    def create(self, validated_data):
        team = createContestants(validated_data, OnlineTeam, OnlineContestant)
        return team

    def validate(self, data):
        if validate_contestants(OnlineContestantSerializer, data['contestants']):
            super_val = super(OnlineTeamSerializer, self).validate(data)
            return super_val
        raise SuspiciousOperation("Invalid contestants!")

class OnlineTeamListSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = OnlineTeam
        fields = online_team_fields


class OnsiteTeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnsiteTeam
        exclude = ('id', )


class OnlineTeamGenerateSerializer(OnlineTeamSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = OnlineTeam
        fields = generate_online_team_fields + ['user', 'password']

    def get_user(self, obj):
        user = generate_user_from_email(obj.contestants.all()[0].email)
        return user

class OnsiteTeamGenerateSerializer(OnsiteTeamSerializer):
    class Meta:
        model = OnsiteTeam
        fields = generate_team_fields


class ContestantGenerateSerializer(serializers.ModelSerializer):
    institution = serializers.SerializerMethodField()
    team = serializers.SlugRelatedField(slug_field='name', read_only=True)

    def get_institution(self, obj):
        return obj.team.institution


class OnsiteContestantGenerateSerializer(ContestantGenerateSerializer):
    class Meta:
        model = OnsiteContestant
        fields = onsite_contestant_fields + generate_contestant_fields


class OnlineContestantGenerateSerializer(ContestantGenerateSerializer):
    class Meta:
        model = OnlineContestant
        fields = contestant_fields + generate_contestant_fields
