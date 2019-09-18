from django.db import models
from photologue.models import Gallery as RawGallery, PhotoSizeCache, PhotoSize
from django.conf import settings
from .photologue_model_override import Photo


class Contest (models.Model):
    year = models.CharField(max_length=4, default="")
    problems = models.CharField(max_length=500) 
    final_ranking_onsite = models.CharField(max_length=500)
    final_ranking_online = models.CharField(max_length=500)
    poster = models.ImageField(verbose_name='poster')

    def __str__(self):
        return 'ACM ' + str(self.year)

# Makes the more recent contest the main one in case the main one is deleted.
# An alternative Approach is commented to prohibit admin from deleting the main contest, having to change it to another one first.


def get_latest_contest():
    return Contest.objects().latest('year')


class CurrentContest(models.Model):
    main = models.ForeignKey(Contest, on_delete=models.SET('get_latest_contest'))

    class Meta:
        verbose_name_plural = 'Current Contest'


class Gallery(RawGallery):
    # Photo title is the team name,
    # Photo caption is the members' name.
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)    

    class Meta:
        verbose_name = 'Contest Gallery'
        verbose_name_plural = 'Contest Galleries'

    def __str__(self):
        return 'ACM ' + self.contest.year + ' ' + self.title
