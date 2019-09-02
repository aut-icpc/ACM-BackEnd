from django.db import models
from photologue.models import Gallery as RawGallery
from photologue.models import Photo as RawPhoto


class Contest (models.Model):
    title = models.CharField(max_length=500)
    problems = models.CharField(max_length=500) 
    final_ranking_onsite = models.CharField(max_length=500)
    final_ranking_online = models.CharField(max_length=550)
    # test_data = models.CharField(max_length=50)
    # judge_solution = models.CharField(max_length = 50)

    def __str__(self):
        return self.title

    # class Meta:
    #     # verbose_name = ''
    #     # verbose_name_plural = ''    

class Gallery(RawGallery):
    # Photo title is the team name,
    # Photo caption is the members' name.
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Contest Gallery'
        verbose_name_plural = 'Contest Galleries'

class Photo(RawPhoto):
    pass
    #For now