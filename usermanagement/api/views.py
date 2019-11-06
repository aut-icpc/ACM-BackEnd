from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
)

from django.db import IntegrityError
from django.core.exceptions import SuspiciousOperation
from .utils import validateRecaptcha

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
    OnlineTeamListSerializer
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

class OnsiteTeamCreateView(CreateAPIView):
    queryset = OnsiteTeam.objects.all()
    serializer_class = OnsiteTeamSerializer


    # def create(self, request, *args, **kwargs):
    #     try:
    #         if validateRecaptcha(request):
    #             return super(OnsiteTeamCreateView, self).create(request, *args, **kwargs)
    #         else:
    #             raise SuspiciousOperation("Invalid recaptcha")
    #     except IntegrityError as err:
    #         raise SuspiciousOperation("Invalid user parameters!")
