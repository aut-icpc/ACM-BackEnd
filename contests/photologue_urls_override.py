from django.conf.urls import url
from django.views.generic import RedirectView
from django.urls import reverse_lazy

from .photologue_views_override import PhotoListView, PhotoDetailView, GalleryListView, \
    GalleryDetailView, PhotoArchiveIndexView, PhotoDateDetailView, PhotoDayArchiveView, \
    PhotoYearArchiveView, PhotoMonthArchiveView, GalleryArchiveIndexView, GalleryYearArchiveView, \
    GalleryDateDetailView, GalleryDayArchiveView, GalleryMonthArchiveView

"""NOTE: the url names are changing. In the long term, I want to remove the 'cn-'
prefix on all urls, and instead rely on an apcnication namespace 'photologue'.

At the same time, I want to change some URL patterns, e.g. for pagination. Changing the urls
twice within a few releases, could be confusing, so instead I am updating URLs bit by bit.

The new style will coexist with the existing 'cn-' prefix for a coucne of releases.

"""


app_name = 'contests'
urlpatterns = [
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
        GalleryDateDetailView.as_view(month_format='%m'),
        name='gallery-detail'),
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
        GalleryDayArchiveView.as_view(month_format='%m'),
        name='gallery-archive-day'),
    url(r'^gallery/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
        GalleryMonthArchiveView.as_view(month_format='%m'),
        name='gallery-archive-month'),
    url(r'^gallery/(?P<year>\d{4})/$',
        GalleryYearArchiveView.as_view(),
        name='cn-gallery-archive-year'),
    url(r'^gallery/$',
        GalleryArchiveIndexView.as_view(),
        name='cn-gallery-archive'),
    url(r'^$',
        RedirectView.as_view(
            url=reverse_lazy('contests:cn-gallery-archive'), permanent=True),
        name='cn-contests-root'),
    url(r'^gallery/(?P<slug>[\-\d\w]+)/$',
        GalleryDetailView.as_view(), name='cn-gallery'),
    url(r'^gallerylist/$',
        GalleryListView.as_view(),
        name='gallery-list'),

    url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
        PhotoDateDetailView.as_view(month_format='%m'),
        name='photo-detail'),
    url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/(?P<day>\w{1,2})/$',
        PhotoDayArchiveView.as_view(month_format='%m'),
        name='photo-archive-day'),
    url(r'^photo/(?P<year>\d{4})/(?P<month>[0-9]{2})/$',
        PhotoMonthArchiveView.as_view(month_format='%m'),
        name='photo-archive-month'),
    url(r'^photo/(?P<year>\d{4})/$',
        PhotoYearArchiveView.as_view(),
        name='cn-photo-archive-year'),
    url(r'^photo/$',
        PhotoArchiveIndexView.as_view(),
        name='cn-photo-archive'),

    url(r'^photo/(?P<slug>[\-\d\w]+)/$',
        PhotoDetailView.as_view(),
        name='cn-photo'),
    url(r'^photolist/$',
        PhotoListView.as_view(),
        name='photo-list'),
]
