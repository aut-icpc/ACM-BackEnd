from django.db import models
from photologue.models import Gallery as RawGallery
from photologue.models import Photo as RawPhoto
from photologue.models import PhotoSize
from django.conf import settings
# from django.db.models.signals import pre_save
# from django.dispatch import receiver

class Contest(models.Model):
    year = models.CharField(max_length=4)
    problems = models.CharField(max_length=500) 
    final_ranking_onsite = models.CharField(max_length=500)
    final_ranking_online = models.CharField(max_length=500)

    def __str__(self):
        return 'ACM ' + str(self.year)


class Photo(RawPhoto):
    # photo = models.OneToOneField(RawPhoto, related_name='contest_photo', on_delete=models.CASCADE)
    thumbnail_size = models.ForeignKey(PhotoSize, related_name='contest_photo', on_delete=models.DO_NOTHING)
    thumbnail_url = models.TextField(verbose_name='thumbnail_url')

    class Meta:
        verbose_name = 'Contest Photo'

    @property
    def get_thumbnail_size(self):
        ts = self.thumbnail_size
        return [ts.height, ts.width]
    
    @property
    def get_photo_src(self):
        return settings.MEDIA_URL + self.image.name

    @property
    def get_thumbnail_url(self):
        # dont forget to add cache
        if len(self.thumbnail_url) == 0:
            file_name = self.get_photo_src
            print(file_name)
            last_dot = file_name.rfind('.')
            photo_name, photo_extension = file_name[:last_dot], file_name[last_dot:]
            self.thumbnail_url = photo_name + '_' + self.thumbnail_size.name + photo_extension
            
        return self.thumbnail_url
    
    # def save(self, *args, **kwargs):

    # def generate_thumbnail_url(sender, **kwargs):
    #     kwargs.get('instance').thumbnail_url = self.get_thumbnail_url()
    #     return 

# @receiver(pre_save, sender=Photo, dispatch_uid="add_thumbnail_url")
# def add_thumbnail_url(sender, instance, **kwargs):
#     instance.get_thumbnail_url()



class Gallery(RawGallery):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='gallery')    

    class Meta:
        verbose_name = 'Contest Gallery'
        verbose_name_plural = 'Contest Galleries'

    def __str__(self):
        return 'ACM ' + self.contest.year + ' ' + self.title
