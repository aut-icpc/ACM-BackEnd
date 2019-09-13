from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView
)

from contests.models import Gallery, Contest, Photo
# from photologue.models import Photo

from .serializers import (
    GallerySerializer,
    ContestSerializer,
    PhotoSerializer
)


class PhotoView(RetrieveAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    
class GalleryRetrieveView(RetrieveAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

class ContestRetrieveView(RetrieveAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
