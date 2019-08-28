from django.db import models


class ACM (models.Model):
    title = models.CharField(max_length=50)
    problems = models.CharField(max_length=20)
    final_ranking_onsite = models.CharField(max_length=20)
    final_ranking_online = models.CharField(max_length=20)
    test_data = models.CharField(max_length=20)
    judge_solution = models.CharField(max_length = 20)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ACM'
        verbose_name_plural = 'ACM CONTEST'    

