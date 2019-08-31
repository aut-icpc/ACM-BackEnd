from rest_framework import serializers
from usermanagement.models import (
    Country,
    Team,
    OnlineContestant,
    OnsiteContestant
)

contestant_fields = ['first_name', 'last_name', 'gender', 'edu_level', 'student_number', 'email', 'phone_number', 'team']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country 
        fields = '__all__'
    
class TeamSerializer(serializers.ModelSerializer):
    # country = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = Team 
        fields = ['name', 'is_onsite', 'status', 'institution', 'country']

class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamListSerializer
        fields = ['name', 'institution', 'status']

class OnsiteContestantSerializer(serializers.ModelSerializer):
    team = serializers.CharField(max_length=255)
    class Meta:
        model = OnsiteContestant
        fields = contestant_fields

    def create(self, validated_data):
        team_name = validated_data.pop('team')
        team = Team.objects.get(name=team_name)
        validated_data.update({
            'team':team
        })
        obj = OnsiteContestant.objects.create(**validated_data)
        obj.save()
        return obj

    

class OnlineContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineContestant 
        fields = contestant_fields
    