from rest_framework import serializers
from contests.models import (
    Gallery,
    Photo
)

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

