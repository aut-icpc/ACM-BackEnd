from django.contrib import admin
from django.utils.html import format_html
from .models import Contest, Gallery, Photo, CurrentContest
from photologue.models import Photo as RawPhoto
from photologue.admin import GalleryAdmin as RawGalleryAdmin, PhotoAdmin as RawPhotoAdmin, PhotoAdminForm as RawPhotoAdminForm
from django import forms
from .photologue_admin_override import PhotoAdmin


def unregister_photologue():
    from photologue.models import Gallery, PhotoEffect, PhotoSize, Watermark
    
    admin.site.unregister(Gallery)
    admin.site.unregister(RawPhoto)
    admin.site.unregister(PhotoEffect)
    admin.site.unregister(Watermark)

unregister_photologue()

admin.site.register(Photo, PhotoAdmin)

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


admin.site.register(CurrentContest)