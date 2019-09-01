from django.urls import path
from .views import (
    ACMTitleistView, ACMRetriveView
)

urlpatterns =[

     path("<pk>",ACMRetriveView.as_view(), name='ACMRET'),
     path("", ACMTitleistView.as_view(), name ='ACMTIT'),
]