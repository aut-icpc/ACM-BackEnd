from rest_framework import serializers
from contests.models import Gallery, Contest
from photologue.models import Photo

class GallerySerializer(serializers.ModelSerializer):
    photos = serializers.ReadOnlyField(source='photo_urls')
    class Meta:
        model = Gallery
        fields = ['title', 'photos']
    
    # def get_photos(self, obj):


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

# If 
