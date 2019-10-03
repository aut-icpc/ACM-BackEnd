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

class TeamAdmin(admin.ModelAdmin):
    change_list_template = 'change_list_onsite_team.html'

    def get_urls(self):
        urls = super(TeamAdmin, self).get_urls()
        custom_urls = [
            url(r'export_teams/$',
            self.admin_site.admin_view(self.export_online_teams),
            name='contests_export_teams')
        ]
        return custom_urls + urls

    def export_online_teams(self, request):
        context = {
            'title': ('Export Onsite Teams'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }
        if request.method == 'POST':
            export_form = ExportTeamForm(request.POST)
            if export_form.is_valid():
                return export_form.save(request=request, classType=self.__class__)
        else:
            export_form = ExportTeamForm()
        context['form'] = export_form
        context['adminform'] = helpers.AdminForm(export_form,
                                                 list([(None, {'fields': export_form.base_fields})]),
                                                 {})

        return render(request, 'select_export.html', context)



class OnlineTeamAdmin(TeamAdmin):
    form = OnlineTeamForm


class OnsiteTeamAdmin(TeamAdmin):
    form = OnsiteTeamForm

    



admin.site.register(OnsiteTeam, OnsiteTeamAdmin)
admin.site.register(OnlineTeam, OnlineTeamAdmin)
admin.site.register(OnlineContestant)
admin.site.register(OnsiteContestant)
admin.site.register(Country)
admin.site.register(MailMessage)