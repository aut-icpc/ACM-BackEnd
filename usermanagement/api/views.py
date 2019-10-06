from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
)

from django.db import IntegrityError
from django.core.exceptions import SuspiciousOperation

from usermanagement.models import (
    Country,
    OnlineTeam,
    OnsiteTeam,
    OnlineContestant,
    OnsiteContestant
)

from .serializers import (
    CountrySerializer,
    OnsiteTeamSerializer,
    OnlineTeamSerializer,
    OnsiteTeamListSerializer,
    OnlineTeamListSerializer,
    OnlineContestantSerializer,
    OnsiteContestantSerializer
)

class CountryListView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class OnlineTeamListView(ListAPIView):
    queryset = OnlineTeam.objects.all()
    serializer_class = OnlineTeamListSerializer

class OnsiteTeamListView(ListAPIView):
    queryset = OnsiteTeam.objects.all()
    serializer_class = OnsiteTeamListSerializer

class OnlineTeamCreateView(CreateAPIView):
    queryset = OnlineTeam.objects.all()
    serializer_class = OnlineTeamSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super(OnlineTeamCreateView, self).create(request, *args, **kwargs)
        except IntegrityError:
            raise SuspiciousOperation

class OnsiteTeamCreateView(CreateAPIView):
    queryset = OnsiteTeam.objects.all()
    serializer_class = OnsiteTeamSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super(OnsiteTeamCreateView, self).create(request, *args, **kwargs)
        except IntegrityError:
            raise SuspiciousOperation
