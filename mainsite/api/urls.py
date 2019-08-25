from django.urls import path

from .views import (
    TimeLineItemListView,
    TimeLineItemDetailView,
    CountDownView
    )

urlpatterns = [
    path('timelineitems', TimeLineItemListView.as_view()),
    path('timelineitems/<pk>', TimeLineItemDetailView.as_view()),
    path('countdowns/<pk>', CountDownView.as_view()),
]