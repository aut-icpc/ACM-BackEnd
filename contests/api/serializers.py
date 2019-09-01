from rest_framework import serializers
from ..models import ACM

class ACMSerializer(serializers.ModelSerializer):    
     class Meta:
        model = ACM
        fields = '__all__'


class ACMTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ACM
        fields = ['title',]
