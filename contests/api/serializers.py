from rest_framework import serializers
from contests.models import Gallery, Contest, Photo
# from photologue.models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    thumbnail_size = serializers.ReadOnlyField(source='get_thumbnail_size')
    src = serializers.ReadOnlyField(source='photo.image.name')
    class Meta:
        model = Photo
        fields = ['thumbnail_size', 'src']


class GallerySerializer(serializers.ModelSerializer):
    # photos = serializers.ReadOnlyField(source='get_photos')
    photos = PhotoSerializer(many=True)
    class Meta:
        model = Gallery
        fields = ['title', 'photos']

class ContestSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True)
    class Meta:
        model = Contest
        fields = ['year', 'problems', 'final_ranking_onsite', 'final_ranking_online', 'gallery']


# class PhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Photo
#         fields = '__all__'

# If i'm a carrot, what happens,
# mate?