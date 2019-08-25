from django.db import models

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


#2019-08-30T00:00:00Z