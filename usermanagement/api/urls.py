from django.urls import path

from .views import (
    CountryListView,
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    OnlineContestantCreateView,
    OnsiteContestantCreateView,
)

urlpatterns = [
    path('countries', CountryListView.as_view()),
    path('teams', TeamListView.as_view()),
    # path('teams/<pk>', TeamDetailView.as_view()),
    path('register/team/', TeamCreateView.as_view()),
    path('register/contestant/online', OnlineContestantCreateView.as_view()),
    path('register/contestant/onsite', OnsiteContestantCreateView.as_view()),
]