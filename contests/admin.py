from django.contrib import admin
from django.utils.html import format_html
from .models import Contest, Gallery, Photo 
from photologue.admin import GalleryAdmin as RawGalleryAdmin, PhotoAdmin as RawPhotoAdmin, PhotoAdminForm as RawPhotoAdminForm
from photologue.models import Photo as RawPhoto, PhotoSize
from photologue.forms import UploadZipForm as RawUploadZipForm
from django.http import HttpResponseRedirect
from django import forms
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib.admin import helpers
from django.shortcuts import render


def unregister_photologue():
    from photologue.models import Gallery, PhotoEffect, PhotoSize, Watermark
    
    admin.site.unregister(Gallery)
    admin.site.unregister(RawPhoto)
    admin.site.unregister(PhotoEffect)
    admin.site.unregister(Watermark)

unregister_photologue()

class ContestAdmin(admin.ModelAdmin):
    list_display = ('year','show_problem',
    'show_final_ranking_onsite' ,'show_final_ranking_online', )
    search_fields = ['year']

    def show_problem(self, obj):
        return format_html("<a href='{url}'>{text}</a>", url=obj.problems , text="problems")
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

class GalleryAdmin(RawGalleryAdmin):
    list_display = ('contest', 'title', 'date_added', 'photo_count', 'is_public')
    form = GalleryAdminForm

admin.site.register(Gallery, GalleryAdmin)


class PhotoInline(admin.StackedInline):
    model = Photo
    can_delete = False
    exclude = ['thumbnail_url']

class GalleryInline(admin.StackedInline):
    model = Gallery
    can_delete = False

class UploadZipForm(RawUploadZipForm):
    thumbnail_size = forms.ModelChoiceField(PhotoSize.objects.all(),
                                     label=_('PhotoSize'),
                                     required=True)


#TODO: add thumbnail_size to zip mode!!

class PhotoAdmin(RawPhotoAdmin):
    inlines = [PhotoInline, ]

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

admin.site.register(RawPhoto, PhotoAdmin)


# class PhotoAdminForm(RawPhotoAdminForm):
#     class Meta:
#         model = Photo
#         fields = '__all__'

# class PhotoAdmin(RawPhotoAdmin):
#     form = PhotoAdminForm

    # def upload_zip(self, request):
    #     return self.super().upload_zip(self, request)

    # def get_urls(self):
    #     return self.super().get_urls()

# admin.site.unregister(Photo)
# admin.site.register(Photo, PhotoAdmin)