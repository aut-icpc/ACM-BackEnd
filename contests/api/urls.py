from django.urls import path

from .views import (
    GalleryRetrieveView,
    ContestRetrieveView,
    ContestListView,
    PhotoView
)

urlpatterns = [
    path('galleries/<pk>', GalleryRetrieveView.as_view()),
    path('contests/<str:year>', ContestRetrieveView.as_view()),
    path('contests', ContestListView.as_view()),
    path('photos/<pk>', PhotoView.as_view())
]