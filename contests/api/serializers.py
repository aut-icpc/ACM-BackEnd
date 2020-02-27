from rest_framework import serializers
from contests.models import Gallery, Contest, Photo, CurrentContest
from django.conf import settings
import os


class PhotoSerializer(serializers.ModelSerializer):
    thumbnail_size = serializers.ListField(read_only=True, source='get_thumbnail_size')
    src = serializers.SerializerMethodField()
    thumbnail_url = serializers.ReadOnlyField(source='get_thumbnail_url')

    class Meta:
        model = Photo
        fields = ['src', 'thumbnail_url', 'thumbnail_size', 'caption']
        depth = 1

    def get_src(self, obj):
        return os.path.join(settings.MEDIA_URL, obj.image.name)


class GallerySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Gallery
        fields = ['title', 'photos']
        depth = 1


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['year', 'problems', 'final_ranking_onsite', 'final_ranking_online', 'poster', 'has_passed']


class ContestGalleriesSerializer(serializers.ModelSerializer):
    galleries = GallerySerializer(many=True)

    class Meta:
        model = Contest
        fields = ['galleries']


class CurrentContestSerializer(serializers.ModelSerializer):
    poster = serializers.ReadOnlyField(source='get_current_poster')
    year = serializers.ReadOnlyField(source='main.year')
    sponsor = serializers.ReadOnlyField(source='get_sponsor')

    class Meta:
        model = CurrentContest
        fields = ['poster', 'year', 'sponsor']
