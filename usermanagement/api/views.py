from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
)

from usermanagement.models import (
    Country,
    Team,
    OnlineContestant,
    OnsiteContestant
)

from .serializers import (
    CountrySerializer,
    TeamSerializer,
    OnlineContestantSerializer,
    OnsiteContestantSerializer
)

class CountryListView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class TeamListView(ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetailView(RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamCreateView(CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class OnlineContestantCreateView(CreateAPIView):
    queryset = OnlineContestant.objects.all()
    serializer_class = OnlineContestantSerializer

class OnsiteContestantCreateView(CreateAPIView):
    queryset = OnsiteContestant.objects.all()
    serializer_class = OnsiteContestantSerializer

# class OnlineContestantDetailView(RetrieveAPIView):
#     queryset = OnlineContestant.objects.all()
#     serializer_class = CountrySerializer
