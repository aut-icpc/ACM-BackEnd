from rest_framework import serializers
from contests.models import Gallery, Contest, Photo

class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    thumbnail_height = serializers.ReadOnlyField(source='thumbnail_size.height')
    thumbnail_width = serializers.ReadOnlyField(source='thumbnail_size.width')
    src = serializers.ReadOnlyField(source='get_photo_src')
    thumbnail_url = serializers.ReadOnlyField(source='get_thumbnail_url')
    caption = serializers.ReadOnlyField(source='photo.caption')
    class Meta:
        model = Photo
        fields = ['src', 'thumbnail_url', 'thumbnail_height', 'thumbnail_width', 'caption']


class GallerySerializer(serializers.ModelSerializer):
    # photos = PhotoSerializer(many=True)
    photos = serializers.ListField(read_only=True, child=PhotoSerializer())
    class Meta:
        model = Gallery
        fields = ['title', 'photos']
        depth = 1


    

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
# mate? People on street
#dada
# class PhotoField(serializers.RelatedField):
#     def to_representation(self, value):
#         src = '"src": %s' % value.src
#         thumbnail_url = '"thumbnail_url": %s' % value.thumbnail_url
#         thumbnail_height = '"thumbnail_height": %s' % value.thumbnail_height
#         thumbnail_width = '"thumbnail_width": %s' % value.thumbnail_width
#         caption = '"thumbnail_url": %s' % value.caption
#         return '{%s, %s, %s, %s, %d}' % src, thumbnail_url, thumbnail_height, thumbnail_width, caption

# photos = serializers.SerializerMethodField()

    # @property
    # def get_photos(self, obj):
    #     photo = {
    #         'src': obj.src,
    #         'thumbnail_url': obj.thumbnail_url,
    #         'thumbnail_height': obj.thumbnail_height,
    #         'thumbnail_width': obj.thumbnail_width,
    #         'caption': obj.caption
    #     }
    #     return photo
        # return PhotoSerializer(many=True).data

    # def get_fields(self):
    #     '''
    #     Override get_fields() method to pass context to other serializers of this base class.

    #     If the context contains query param "omit_data" as set to true, omit the "data" field
    #     '''
    #     fields = super().get_fields()

    #     # Cause fields with this same base class to inherit self._context
    #     for field_name in fields:
    #         if isinstance(fields[field_name], serializers.ListSerializer):
    #             if isinstance(fields[field_name].child, PhotoSerializer):
    #                 fields[field_name].child._context = self._context

    #         elif isinstance(fields[field_name], PhotoSerializer):
    #             fields[field_name]._context = self._context

    #     # Check for "omit_data" in the query params and remove data field if true
    #     if 'request' in self._context:
    #         omit_data = self._context['request'].query_params.get('omit_data', False)

    #         if omit_data and omit_data.lower() in ['true', '1']:
    #             fields.pop('data')

    #     return fields

    
    # def get_fields(self):
    #     obj = super().get_fields()
    #     # obj.update({
    #     #     "mamad": "mamad"
    #     # })
    #     # print( obj['photos']._kwargs['child']['src'])
    #     print(obj['photos'])
    #     print(obj)
    #     return obj

    # def get_photos(self, obj):
        