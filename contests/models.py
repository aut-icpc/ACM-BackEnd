from django.db import models
from django.contrib.postgres.fields import ArrayField
from sorl.thumbnail import ImageField
from sorl.thumbnail import get_thumbnail
from sorl.thumbnail import delete


class ACM (models.Model):
    title = models.CharField(max_length=500)
    problems = models.CharField(max_length=500) 
    final_ranking_onsite = models.CharField(max_length=500)
    final_ranking_online = models.CharField(max_length=550)
    poster = models.CharField(max_length= 500,blank=True, null=True)
   

  
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'CONTEST'
        verbose_name_plural = 'CONTESTS'    

class Image(models.Model):
    # in alakie baad kelass mokhstam check konam
    im = get_thumbnail(my_file, '300x400', crop='center', quality=99)
    
    # src = models.CharField(max_length = 500)
    # thumbnail = models.CharField(max_length = 500)
    # thumbnailheight = 300   
    # thumbnailwidth = 400
    contest = models.ForeignKey(ACM, blank=True, null=True , related_name="contest" , on_delete= models.CASCADE)
    def __str__(self):
        return self.src


