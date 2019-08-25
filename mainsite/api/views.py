from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from mainsite.models import (
    TimeLineItem,
    Countdown,
    )
from .serializers import (
    TimeLineItemSerializer,
    CountdownSerializer,
)


class TimeLineItemListView(ListAPIView):
    queryset = TimeLineItem.objects.all()
    serializer_class = TimeLineItemSerializer

class TimeLineItemDetailView(RetrieveAPIView):
    queryset = TimeLineItem.objects.all()
    serializer_class = TimeLineItemSerializer

class CountDownView(RetrieveAPIView):
    queryset = Countdown.objects.all()
    serializer_class = CountdownSerializer