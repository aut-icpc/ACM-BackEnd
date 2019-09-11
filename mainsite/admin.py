from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from photologue.models import Gallery, Photo, PhotoEffect, PhotoSize, Watermark

from .models import (
    TimeLineItem,
    Countdown
)

# Register your models here.

admin.site.register(TimeLineItem)
admin.site.register(Countdown)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(FlatPage)
admin.site.unregister(Site)
admin.site.unregister(Gallery)
admin.site.unregister(Photo)
admin.site.unregister(PhotoEffect)
admin.site.unregister(PhotoSize)
admin.site.unregister(Watermark)