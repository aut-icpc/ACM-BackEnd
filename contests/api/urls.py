from django.urls import path

from .views import (
    GalleryRetrieveView,
    ContestRetrieveView,
    PhotoView
)

urlpatterns = [
    path('galleries/<pk>', GalleryRetrieveView.as_view()),
    path('contests/<pk>', ContestRetrieveView.as_view()),
    path('photos/<pk>', PhotoView.as_view())
]