from django.db import models
from django.conf import settings
from photologue.models import Gallery as RawGallery, Photo as RawPhoto, PhotoSizeCache, PhotoSize, IMAGE_EXIF_ORIENTATION_MAP
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from pathlib import Path
from collections import OrderedDict


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

    @property
    def get_current_poster(self):
        return settings.MEDIA_URL + main.poster.name

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        super(CurrentContest, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        pass


class Gallery(RawGallery):
    # Photo title is the team name,
    # Photo caption is the members' name.
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)    

    class Meta:
        verbose_name = 'Contest Gallery'
        verbose_name_plural = 'Contest Galleries'

    def __str__(self):
        return 'ACM ' + self.contest.year + ' ' + self.title

class Photo(RawPhoto):
    thumbnail_size = models.ForeignKey(PhotoSize, related_name='contest_photo', on_delete=models.DO_NOTHING)
    thumbnail_url = models.TextField(verbose_name='thumbnail_url')


    thumbnail_urls = OrderedDict()

    class Meta:
        verbose_name = 'Contest Photo'

    @property
    def get_thumbnail_url(self):
        return self.thumbnail_url

    @property
    def get_thumbnail_size(self):
        ts = self.thumbnail_size
        return [ts.height, ts.width]

    def set_thumbnail_url(self):
        if len(self.thumbnail_url) == 0:
            self.thumbnail_url = self.thumbnail_urls[self.thumbnail_size.name]
        print(self.thumbnail_url)

        return self.thumbnail_url

    
    def pre_cache(self):
        photosize = self.thumbnail_size
        if photosize.pre_cache:
            photosize_url = self.create_size(photosize)
            # Create serializable address
            photosize_dir = str(photosize_url)
            # Windows compatibility in debug mode.
            photosize_win_dir = photosize_dir.replace("\\", "/")
            if photosize.name not in self.thumbnail_urls.keys() and photosize_win_dir != "None":
                self.thumbnail_urls.update({
                    photosize.name: settings.MEDIA_URL + photosize_win_dir
                })
        
    

    def create_size(self, photosize):
        if self.size_exists(photosize):
            return
        try:
            im = Image.open(self.image.storage.open(self.image.name))
        except IOError:
            return
        # Save the original format
        im_format = im.format
        # Apply effect if found
        if self.effect is not None:
            im = self.effect.pre_process(im)
        elif photosize.effect is not None:
            im = photosize.effect.pre_process(im)
        # Rotate if found & necessary
        if 'Image Orientation' in self.EXIF() and \
                self.EXIF().get('Image Orientation').values[0] in IMAGE_EXIF_ORIENTATION_MAP:
            im = im.transpose(
                IMAGE_EXIF_ORIENTATION_MAP[self.EXIF().get('Image Orientation').values[0]])
        # Resize/crop image
        if im.size != photosize.size and photosize.size != (0, 0):
            im = self.resize_image(im, photosize)
        # Apply watermark if found
        if photosize.watermark is not None:
            im = photosize.watermark.post_process(im)
        # Apply effect if found
        if self.effect is not None:
            im = self.effect.post_process(im)
        elif photosize.effect is not None:
            im = photosize.effect.post_process(im)
        # Save file
        im_filename = getattr(self, "get_%s_filename" % photosize.name)()
        try:
            buffer = BytesIO()
            # Issue #182 - test fix from https://github.com/bashu/django-watermark/issues/31
            if im.mode.endswith('A'):
                im = im.convert(im.mode[:-1])
            if im_format != 'JPEG':
                im.save(buffer, im_format)
            else:
                im.save(buffer, 'JPEG', quality=int(photosize.quality),
                        optimize=True)
            buffer_contents = ContentFile(buffer.getvalue())
            self.image.storage.save(im_filename, buffer_contents)
        except IOError as e:
            if self.image.storage.exists(im_filename):
                self.image.storage.delete(im_filename)
            raise e
        # This returns the thumbnail's url
        return Path(im_filename)
