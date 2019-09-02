from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView
)

from contests.models import (
    Gallery,
    Photo
)

from .serializers import (
    GallerySerializer,
    PhotoSerializer
)

class GalleryRetrieveView(RetrieveAPIView):
    