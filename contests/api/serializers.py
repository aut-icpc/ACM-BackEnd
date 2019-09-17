from rest_framework import serializers
from contests.models import Gallery, Contest, Photo

class PhotoSerializer(serializers.ModelSerializer):
    thumbnail_size = serializers.ListField(read_only=True, source='get_thumbnail_size')
    caption = serializers.ReadOnlyField(source='photo.caption')
    class Meta:
        model = Photo
        fields = ['src', 'thumbnail_url', 'thumbnail_size', 'caption']


class GallerySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    class Meta:
        model = Gallery
        fields = ['title', 'photos']

   

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ['year', 'problems', 'final_ranking_onsite', 'final_ranking_online']
