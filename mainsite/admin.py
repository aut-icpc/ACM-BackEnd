from django.contrib import admin

from .models import (
    TimeLineItem,
    Countdown
)

# Register your models here.

admin.site.register(TimeLineItem)
admin.site.register(Countdown)