from django.db import models
from photologue.models import Gallery as RawGallery
from photologue.models import Photo as RawPhoto
from photologue.models import PhotoSize
from django.conf import settings

class Contest (models.Model):
    year = models.CharField(max_length=4, default="")
    problems = models.CharField(max_length=500) 
    final_ranking_onsite = models.CharField(max_length=500)
    final_ranking_online = models.CharField(max_length=500)

    def __str__(self):
        return 'ACM ' + str(self.year)


class Photo(models.Model):
    photo = models.OneToOneField(RawPhoto, related_name='contest_photo', on_delete=models.CASCADE)
    thumbnail_size = models.OneToOneField(PhotoSize, related_name='contest_photo', on_delete=models.CASCADE)
    thumbnail_url = models.TextField(verbose_name='thumbnail_url')

    class Meta:
        verbose_name = 'Contest Photo'

    @property
    def get_thumbnail_size(self):
        ts = self.thumbnail_size
        return ts.height, ts.width


class Gallery(RawGallery):
    # Photo title is the team name,
    # Photo caption is the members' name.
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='gallery')    

    class Meta:
        verbose_name = 'Contest Gallery'
        verbose_name_plural = 'Contest Galleries'

    def __str__(self):
        return 'ACM ' + self.contest.year + ' ' + self.title

    @property
    def get_photos(self):
        images = []
        urls = []
        for photo in RawPhoto.objects.filter(galleries=self.pk):
            images.append({
                "src": settings.MEDIA_URL + photo.image.name
            })
            # urls += [settings.MEDIA_URL + photo.image.name]
        return urls
