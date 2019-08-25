from rest_framework import serializers
from mainsite.models import (
    TimeLineItem,
    Countdown,
)

class TimeLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLineItem
        fields = ['dateText', 'style', 'dateInnerStyle',
         'title', 'innerHTML']

class CountdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countdown 
        fields = ['stopTime',]