from django.contrib import admin
from django.utils.html import format_html
from .models import (Contest, Gallery)
# from photologue.models import Photo
from photologue.admin import GalleryAdmin as RawGalleryAdmin
from photologue.admin import PhotoAdmin as RawPhotoAdmin
from django import forms

class ContestAdmin(admin.ModelAdmin):
    # list_display_link = ('title', )
    list_display = ('year','show_problem',
    'show_final_ranking_onsite' ,'show_final_ranking_online', )
    # list_filter = ('title',)
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

# class PhotoAdminForm(forms.ModelForm):
#     class Meta:
#         model = Photo
#         fields = '__all__'

# class PhotoAdmin(RawPhotoAdmin):
#     form = PhotoAdminForm

# admin.site.unregister(Photo)
# admin.site.register(Photo, PhotoAdmin)