from photologue.forms import UploadZipForm as RawUploadZipForm
from django.http import HttpResponseRedirect
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib.admin import helpers
from django.shortcuts import render
from django.conf.urls import url
from django import forms
from photologue.models import Photo as RawPhoto, PhotoSize
from photologue.admin import GalleryAdmin as RawGalleryAdmin, PhotoAdmin as RawPhotoAdmin
import logging
from django.conf import settings
from django.contrib.sites.models import Site
from io import BytesIO
from PIL import Image
import zipfile
from zipfile import BadZipFile
from django.template.defaultfilters import slugify
from .models import Photo, Gallery
from django.contrib import messages
from django.utils.encoding import force_text
from django.core.files.base import ContentFile
import os



logger = logging.getLogger('photologueOverride.forms')

class UploadZipForm(RawUploadZipForm):
    thumbnail_size = forms.ModelChoiceField(PhotoSize.objects.all(),
                                     label=_('PhotoSize'),
                                     required=True)

    def save(self, request=None, zip_file=None):
        if not zip_file:
            zip_file = self.cleaned_data['zip_file']
        zip = zipfile.ZipFile(zip_file)
        count = 1
        current_site = Site.objects.get(id=settings.SITE_ID)
        if self.cleaned_data['gallery']:
            logger.debug('Using pre-existing gallery.')
            gallery = self.cleaned_data['gallery']
        else:
            logger.debug(
                force_text('Creating new gallery "{0}".').format(self.cleaned_data['title']))
            gallery = Gallery.objects.create(title=self.cleaned_data['title'],
                                             slug=slugify(self.cleaned_data['title']),
                                             description=self.cleaned_data['description'],
                                             is_public=self.cleaned_data['is_public'])
            gallery.sites.add(current_site)
        for filename in sorted(zip.namelist()):

            logger.debug('Reading file "{0}".'.format(filename))

            if filename.startswith('__') or filename.startswith('.'):
                logger.debug('Ignoring file "{0}".'.format(filename))
                continue

            if os.path.dirname(filename):
                logger.warning('Ignoring file "{0}" as it is in a subfolder; all images should be in the top '
                               'folder of the zip.'.format(filename))
                if request:
                    messages.warning(request,
                                     _('Ignoring file "{filename}" as it is in a subfolder; all images should '
                                       'be in the top folder of the zip.').format(filename=filename),
                                     fail_silently=True)
                continue

            data = zip.read(filename)

            if not len(data):
                logger.debug('File "{0}" is empty.'.format(filename))
                continue

            photo_title_root = self.cleaned_data['title'] if self.cleaned_data['title'] else gallery.title

            # A photo might already exist with the same slug. So it's somewhat inefficient,
            # but we loop until we find a slug that's available.
            while True:
                photo_title = ' '.join([photo_title_root, str(count)])
                slug = slugify(photo_title)
                if Photo.objects.filter(slug=slug).exists():
                    count += 1
                    continue
                break

            # here it differs from the main source, it has added the thumbnail_size attr to the photo
            photo = Photo(title=photo_title,
                          slug=slug,
                          caption=self.cleaned_data['caption'],
                          is_public=self.cleaned_data['is_public'],
                          thumbnail_size=self.cleaned_data['thumbnail_size'])
            # Basic check that we have a valid image.
            try:
                file = BytesIO(data)
                opened = Image.open(file)
                opened.verify()
            except Exception:
                # Pillow doesn't recognize it as an image.
                # If a "bad" file is found we just skip it.
                # But we do flag this both in the logs and to the user.
                logger.error('Could not process file "{0}" in the .zip archive.'.format(
                    filename))
                if request:
                    messages.warning(request,
                                     _('Could not process file "{0}" in the .zip archive.').format(
                                         filename),
                                     fail_silently=True)
                continue

            contentfile = ContentFile(data)
            photo.image.save(filename, contentfile)
            photo.save()
            photo.sites.add(current_site)
            gallery.photos.add(photo)
            count += 1

        zip.close()

        if request:
            messages.success(request,
                             _('The photos have been added to gallery "{0}".').format(
                                 gallery.title),
                             fail_silently=True)


class PhotoAdmin(RawPhotoAdmin):

    def get_urls(self):
        urls = super(PhotoAdmin, self).get_urls()
        custom_urls = [
            url(r'^upload_zip/$',
                self.admin_site.admin_view(self.upload_zip),
                name='contests_upload_zip')
        ]
        return custom_urls + urls
    
    def upload_zip(self, request):

        context = {
            'title': _('Upload a zip archive of photos'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        # Handle form request
        if request.method == 'POST':
            form = UploadZipForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request=request)
                return HttpResponseRedirect('..')
        else:
            form = UploadZipForm()
        context['form'] = form
        context['adminform'] = helpers.AdminForm(form,
                                                 list([(None, {'fields': form.base_fields})]),
                                                 {})
        return render(request, 'admin/photologue/photo/upload_zip.html', context)
