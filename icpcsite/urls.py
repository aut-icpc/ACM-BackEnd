"""icpcsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from photologue.models import Photo
from django.views.generic import CreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mainsite.api.urls')),
    path('api/', include('usermanagement.api.urls')),
    path('api/', include('contests.api.urls')),
    path(r'contests/', include('contests.urls')),
    # path(r'photologue/', include('photologue.urls')),
    # path(r'photologue/photo/add/', CreateView.as_view(model=Photo), name='add-photo'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
