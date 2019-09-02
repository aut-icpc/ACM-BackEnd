from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    ListAPIView,
)

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

class OnsiteTeamCreateView(CreateAPIView):
    queryset = OnsiteTeam.objects.all()
    serializer_class = OnsiteTeamSerializer



# class FullTeams
# class OnlineContestantCreateView(CreateAPIView):
#     queryset = OnlineContestant.objects.all()
#     serializer_class = OnlineContestantSerializer

# class OnsiteContestantCreateView(CreateAPIView):
#     queryset = OnsiteContestant.objects.all()
#     serializer_class = OnsiteContestantSerializer

