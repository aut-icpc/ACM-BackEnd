from django.urls import path

from .views import (
    CountryListView,
    OnlineTeamListView,
    OnsiteTeamListView,
    OnlineTeamCreateView,
    OnsiteTeamCreateView
)

urlpatterns = [
    path('countries', CountryListView.as_view()),
    path('teams/online', OnlineTeamListView.as_view()),
    path('teams/onsite', OnsiteTeamListView.as_view()),
    path('register/team/onsite', OnsiteTeamCreateView.as_view()),
    path('register/team/online', OnlineTeamCreateView.as_view())

]