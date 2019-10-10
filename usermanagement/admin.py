from django.contrib import admin
from django.conf.urls import url
from django.shortcuts import render
from django.contrib.admin import helpers
from .models import (
    OnlineTeam,
    OnsiteTeam,
    OnlineContestant,
    OnsiteContestant,
    Country,
    Team,
    MailMessage
)

from .forms import (
    OnlineTeamForm,
    OnsiteTeamForm,
    ExportTeamForm,
)

from .api.serializers import (
    OnlineTeamListSerializer,
    OnsiteTeamListSerializer
)

# Register your models here.

# class TeamAdmin(admin.ModelAdmin):
    # change_list_template = 'change_list_team.html'

    # def get_urls(self):
    #     urls = super(TeamAdmin, self).get_urls()
    #     custom_urls = [
    #         url(r'export_teams/$',
    #         self.admin_site.admin_view(self.export_teams),
    #         name='contests_export_teams')
    #     ]
    #     return custom_urls + urls

    # def export_teams(self, request):
    #     context = {
    #         'title': ('Export Teams'),
    #         'app_label': self.model._meta.app_label,
    #         'opts': self.model._meta,
    #         'has_change_permission': self.has_change_permission(request)
    #     }
    #     if request.method == 'POST':
    #         export_form = ExportTeamForm(request.POST)
    #         if export_form.is_valid():
    #             # raise Exception(self.__class__)
    #             return export_form.save(classType=self.__class__)
    #     else:
    #         export_form = ExportTeamForm()
    #     context['form'] = export_form
    #     context['adminform'] = helpers.AdminForm(export_form,
    #                                              list([(None, {'fields': export_form.base_fields})]),
    #                                              {})

    #     return context


class OnsiteTeamAdmin(admin.ModelAdmin):
    
    change_list_template = 'change_list_onsite_team.html'

    form = OnsiteTeamForm

    def export_onsite_teams(self, request):
        context = {
            'title': ('Export Onsite Teams'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }
        if request.method == 'POST':
            export_form = ExportTeamForm(request.POST)
            if export_form.is_valid():
                return export_form.save(classType=self.__class__)
        else:
            export_form = ExportTeamForm()
        context['form'] = export_form
        context['adminform'] = helpers.AdminForm(export_form,
                                                 list([(None, {'fields': export_form.base_fields})]),
                                                 {})
        return render(request, "onsite_export.html", context)

    def get_urls(self):
        urls = super(OnsiteTeamAdmin, self).get_urls()
        custom_urls = [
            url(r'export_teams/$',
            self.admin_site.admin_view(self.export_onsite_teams),
            name='contests_export_onsite_teams')
        ]
        return custom_urls + urls
    

class OnlineTeamAdmin(admin.ModelAdmin):

    change_list_template = 'change_list_online_team.html'
    form = OnlineTeamForm

    def export_online_teams(self, request):
        context = {
            'title': ('Export Online Teams'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }
        if request.method == 'POST':
            export_form = ExportTeamForm(request.POST)
            if export_form.is_valid():
                return export_form.save(classType=self.__class__)
        else:
            export_form = ExportTeamForm()
        context['form'] = export_form
        context['adminform'] = helpers.AdminForm(export_form,
                                                 list([(None, {'fields': export_form.base_fields})]),
                                                 {})
        return render(request, "online_export.html", context)


    def get_urls(self):
        urls = super(OnlineTeamAdmin, self).get_urls()
        custom_urls = [
            url(r'export_teams/$',
            self.admin_site.admin_view(self.export_online_teams),
            name='contests_export_online_teams')
        ]
        return custom_urls + urls




admin.site.register(OnsiteTeam, OnsiteTeamAdmin)
admin.site.register(OnlineTeam, OnlineTeamAdmin)
admin.site.register(OnlineContestant)
admin.site.register(OnsiteContestant)
admin.site.register(Country)
admin.site.register(MailMessage)