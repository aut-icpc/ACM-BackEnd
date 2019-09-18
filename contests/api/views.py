from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView
)

from contests.models import Gallery, Contest, Photo, CurrentContest

from .serializers import (
    GallerySerializer,
    ContestSerializer,
    PhotoSerializer,
    CurrentContestSerializer
)

class PhotoView(RetrieveAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class GalleryRetrieveView(RetrieveAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

class ContestRetrieveView(RetrieveAPIView):
    queryset = Contest.objects.all()
    serializer_class = PhotoSerializer

class ContestListView(ListAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer

class CurrentContestView(RetrieveAPIView):
    queryset = CurrentContest.objects.get()
    serializer_class = CurrentContestSerializer