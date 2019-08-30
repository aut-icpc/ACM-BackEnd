from rest_framework import serializers
from usermanagement.models import (
    Country,
    Team,
    OnlineContestant,
    OnsiteContestant
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country 
        fields = '__all__'
    
class TeamSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = Team 
        # fields = '__all__'
        fields = ['name', 'is_onsite', 'status', 'institution', 'country']

class OnlineContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineContestant 
        fields = '__all__'
    

class OnsiteContestantSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnsiteContestant 
        fields = '__all__'
    
