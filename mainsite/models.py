from django.db import models
from django.core.validators import ValidationError
from ckeditor.fields import RichTextField

# Create your models here.


class TimeLineItem(models.Model):
    dateText = models.TextField()
    style = models.TextField()
    dateInnerStyle = models.TextField()
    title = models.TextField()
    innerHTML = models.TextField()

    def __str__(self):
        return self.title


class Countdown(models.Model):
    stopTime = models.DateTimeField()

    def __str__(self):
        return "Homepage countdown time"

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Countdown, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass
