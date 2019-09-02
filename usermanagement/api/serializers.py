from rest_framework import serializers
from usermanagement.models import (
    Country,
    OnlineTeam,
    OnsiteTeam,
    OnlineContestant,
    OnsiteContestant
)

contestant_fields = ['first_name', 'last_name', 'gender', 
'edu_level', 'student_number', 'email', 'phone_number']
team_fields = ['name', 'status', 'institution', 'contestants']

class OnsiteContestantSerializer(serializers.ModelSerializer):
    # team = serializers.CharField(max_length=255)
    class Meta:
        model = OnsiteContestant
        # exclude = ('team',)
        fields = contestant_fields

    
class OnlineContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineContestant 
        fields = contestant_fields
 

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country 
        fields = '__all__'
    
class OnsiteTeamSerializer(serializers.ModelSerializer):
    contestants = OnsiteContestantSerializer(many=True)
    class Meta:
        model = OnsiteTeam
        fields = team_fields

    def create(self, validated_data):
        contestants_data = validated_data.pop('contestants')
        team = OnsiteTeam.objects.create(**validated_data)
        email = contestants_data[0]['email']
        # print("email: " + email)
        for contestant_data in contestants_data:
            OnsiteContestant.objects.create(team=team, **contestant_data)
        return team

class OnlineTeamSerializer(serializers.ModelSerializer):
    contestants = OnlineContestantSerializer(many=True)
    class Meta:
        model = OnlineTeam
        fields = team_fields + ['country']

    def create(self, validated_data):
        contestants_data = validated_data.pop('contestants')
        team = OnlineTeam.objects.create(**validated_data)
        email = contestants_data[0]['email']
        for contestant_data in contestants_data:
            OnlineContestant.objects.create(team=team, **contestant_data)
        return team


class OnlineTeamListSerializer(serializers.ModelSerializer):
    country = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = OnlineTeam
        fields = ['name', 'institution', 'status', 'country']


class OnsiteTeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnsiteTeam
        fields = '__all__'
    



    # def create(self, validated_data):
    #     team_name = validated_data.pop('team')
    #     team = Team.objects.get(name=team_name)
    #     validated_data.update({
    #         'team':team
    #     })
    #     obj = OnsiteContestant.objects.create(**validated_data)
    #     obj.save()
    #     return obj

# phone_regex = RegexValidator(regex="09[0-9]{9}", message="Phone number must be entered correctly.")
# phone_number = models.CharField(validators=[phone_regex], max_length=12, unique=True)