from django.db import models
from photologue.models import Gallery as RawGallery, Photo as RawPhoto, PhotoSizeCache, PhotoSize
from django.conf import settings
from .photologue_model_override import Photo


class Contest(models.Model):
    year = models.CharField(max_length=4)
    problems = models.CharField(max_length=500) 
    final_ranking_onsite = models.CharField(max_length=500)
    final_ranking_online = models.CharField(max_length=500)

    def __str__(self):
        return 'ACM ' + str(self.year)

# Makes the more recent contest the main one in case the main one is deleted.
# An alternative Approach is commented to prohibit admin from deleting the main contest, having to change it to another one first.

def get_latest_contest():
    return Contest.objects().latest('year')

class CurrentContest(models.Model):
    main = models.ForeignKey(Contest, 
        on_delete=models.SET('get_latest_contest'))
      # on_delete=models.PROTECT()

    class Meta:
        verbose_name_plural = 'Current Contest'


class Gallery(RawGallery):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='gallery')    

    class Meta:
        verbose_name = 'Contest Gallery'
        verbose_name_plural = 'Contest Galleries'

    def __str__(self):
        return 'ACM ' + self.contest.year + ' ' + self.title


# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# @receiver(pre_save, sender=Photo, dispatch_uid="add_thumbnail_url")
# def add_thumbnail_url(sender, instance, **kwargs):
#     instance.get_thumbnail_url()

