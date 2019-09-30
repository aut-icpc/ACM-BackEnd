from django.contrib import admin
from django.utils.html import format_html
from .models import Contest, Gallery, Photo, CurrentContest
from photologue.models import Photo as RawPhoto
from photologue.admin import GalleryAdmin as RawGalleryAdmin, PhotoAdmin as RawPhotoAdmin, PhotoAdminForm as RawPhotoAdminForm
from django import forms
from .forms import PhotoAdminForm, UploadZipForm
import logging
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.contrib.admin import helpers
from django.shortcuts import render


logger = logging.getLogger('contests.admin')


def unregister_photologue():
    from photologue.models import Gallery, PhotoEffect, PhotoSize, Watermark

    admin.site.unregister(Gallery)
    admin.site.unregister(RawPhoto)
    admin.site.unregister(PhotoEffect)
    admin.site.unregister(Watermark)

unregister_photologue()


class ContestAdmin(admin.ModelAdmin):
    list_display = ('year', 'show_problem', 'show_final_ranking_onsite', 'show_final_ranking_online', )
    search_fields = ['year ']

    def show_problem(self, obj):
        return format_html("<a href='{url}'>{text}</a>", url=obj.problems, text="problems")
    show_problem.short_description = "problems"

    def show_final_ranking_onsite(self, obj):
        return format_html("<a href='{url}'>{text}</a>", url=obj.final_ranking_onsite, text="ranking onsite")
    show_final_ranking_onsite.short_description = " final ranking onsite"

    def show_final_ranking_online(self, obj):
        return format_html("<a href='{url}'>{text}</a>", url=obj.final_ranking_online, text="ranking online")
    show_final_ranking_online.short_description = " final ranking online"

admin.site.register(Contest, ContestAdmin)


class GalleryAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    class Meta:
        model = Gallery
        exclude = ['description', 'sites']

    # def __init__(self, *args, **kwargs):


class GalleryAdmin(RawGalleryAdmin):
    list_display = ('contest', 'title', 'date_added', 'photo_count', 'is_public')
    form = GalleryAdminForm


class PhotoAdmin(RawPhotoAdmin):

    change_list_template = 'change_list.html'
    form = PhotoAdminForm
    exclude = ['thumbnail_url', 'sites', 'src']

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
            'title': ('Upload a zip archive of photos'),
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
        return render(request, 'upload_zip.html', context)


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(CurrentContest)
admin.site.register(Photo, PhotoAdmin)
