from rest_framework import serializers
from mainsite.models import (
    TimeLineItem,
    Countdown,
)


class TimeLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLineItem
        fields = '__all__'

class CountdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countdown
        fields = ['stopTime', ]