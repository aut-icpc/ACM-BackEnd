from django.db import models
from django.conf import settings
from photologue.models import Gallery as RawGallery, Photo as RawPhoto, PhotoSizeCache, PhotoSize, IMAGE_EXIF_ORIENTATION_MAP
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from pathlib import Path
from collections import OrderedDict



class Photo(RawPhoto):
    # photo = models.OneToOneField(RawPhoto, related_name='contest_photo', on_delete=models.CASCADE)
    thumbnail_size = models.ForeignKey(PhotoSize, related_name='contest_photo', on_delete=models.DO_NOTHING)
    thumbnail_url = models.TextField(verbose_name='thumbnail_url')
    src = models.TextField(verbose_name='src')


    thumbnail_urls = OrderedDict()

    class Meta:
        verbose_name = 'Contest Photo'

    @property
    def get_thumbnail_size(self):
        ts = self.thumbnail_size
        return [ts.height, ts.width]
    
    @property
    def get_photo_src(self):
        print("oomad inja")
        if len(self.src) == 0:
            self.src = settings.MEDIA_URL + self.image.name
        return self.src

    @property
    def get_thumbnail_url(self):
        print("inja ham oomad")
        if len(self.thumbnail_url) == 0:
            self.thumbnail_url = self.thumbnail_urls[self.thumbnail_size.name]
            
        return self.thumbnail_url
    
    def pre_cache(self):
        cache = PhotoSizeCache()
        for photosize in cache.sizes.values():
            if photosize.pre_cache:
                photosize_url = self.create_size(photosize)
                # Create serializable address
                photosize_dir = str(photosize_url)
                # Windows compatibility in debug mode.
                photosize_win_dir = photosize_dir.replace("\\", "/")
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

    # def save(self, *args, **kwargs):
    #     print("OOOOOOOOOOOOOOMADEEEEEEEEE INJAAAAAAAA")
    #     print(*args)
    #     print(**kwargs)
    #     super().save(*args, **kwargs)
