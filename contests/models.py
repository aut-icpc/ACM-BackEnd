from django.db import models
from photologue.models import Gallery as RawGallery
from photologue.models import Photo as RawPhoto

class Contest (models.Model):
    year = models.CharField(max_length=4, default="")
    problems = models.CharField(max_length=500) 
    final_ranking_onsite = models.CharField(max_length=500)
    final_ranking_online = models.CharField(max_length=500)

    def __str__(self):
        return 'ACM ' + str(self.year)

class Photo(RawPhoto):
    class Meta:
        verbose_name = 'Contest Photo'
    #For now

class Gallery(RawGallery):
    # Photo title is the team name,
    # Photo caption is the members' name.
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Contest Gallery'
        verbose_name_plural = 'Contest Galleries'

    def __str__(self):
        return 'ACM ' + self.contest.year + ' ' + self.title
