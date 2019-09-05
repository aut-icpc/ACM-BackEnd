from rest_framework import serializers
from contests.models import Gallery, Contest
from photologue.models import Photo

class GallerySerializer(serializers.ModelSerializer):
    photos = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='image'
    )
    class Meta:
        model = Gallery
        fields = ['title', ]


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

# class PhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Photo
#         fields = '__all__'

