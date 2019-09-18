from rest_framework import serializers
from contests.models import Gallery, Contest, Photo
from django.conf import settings

class PhotoSerializer(serializers.ModelSerializer):
    thumbnail_size = serializers.ListField(read_only=True, source='get_thumbnail_size')
    # caption = serializers.ReadOnlyField(source='caption')
    # src = serializers.ReadOnlyField(source='photo.image.name')
    # src = serializers.ReadOnlyField()
    src = serializers.SerializerMethodField()
    # photo_src = serializers.ReadOnlyField(source='src', label='src')
    thumbnail_url = serializers.ReadOnlyField(source='get_thumbnail_url')
    class Meta:
        model = Photo
        fields = ['src', 'thumbnail_url', 'thumbnail_size', 'caption']
        depth = 1

    def get_src(self, obj):
        return settings.MEDIA_URL + obj.image.name



class GallerySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    class Meta:
        model = Gallery
        fields = ['title', 'photos']
        depth = 1

    def to_representation(self, obj):
        data = super().to_representation(obj)
        return data


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['year', 'problems', 'final_ranking_onsite', 'final_ranking_online', 'poster']

class ContestGalleriesSerializer(serializers.ModelSerializer):
    galleries = GallerySerializer(many=True)
    class Meta:
        model = Contest
        fields = ['galleries']
