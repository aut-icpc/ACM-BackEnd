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
    MailMessageForm,
    ExportTeamForm,
    SendCustomEmailForm,
)

from .api.serializers import (
    OnlineTeamListSerializer,
    OnsiteTeamListSerializer
)

# Register your models here.

class TeamAdmin(admin.ModelAdmin):
    change_list_template = 'change_list_team.html'
    export_template = ""

    list_display = ['name', 'institution', 'status']

    def name(self, obj):
        return obj.name

    def institution(self, obj):
        return obj.institution
    
    def status(self, obj):
        return obj.status

    def get_urls(self):
        urls = super(TeamAdmin, self).get_urls()
        custom_urls = [
            url(r'export_teams/$',
            self.admin_site.admin_view(self.export_teams),
            name='usermanagement_export_teams')
        ]
        return custom_urls + urls

    def export_teams(self, request):
        context = {
            'title': ('Export Teams'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }
        if request.method == 'POST':
            export_form = ExportTeamForm(request.POST)
            if export_form.is_valid():
                # raise Exception(self.__class__)
                return export_form.save(adminType=self.__class__)
        else:
            export_form = ExportTeamForm()
        context['form'] = export_form
        context['adminform'] = helpers.AdminForm(export_form,
                                                 list([(None, {'fields': export_form.base_fields})]),
                                                 {})

        return render(request, self.export_template, context)


class OnsiteTeamAdmin(TeamAdmin):
    
    change_list_template = 'change_list_onsite_team.html'
    export_template = "onsite_export.html"

    form = OnsiteTeamForm

    def get_urls(self):
        urls = super(OnsiteTeamAdmin, self).get_urls()
        custom_urls = [
            url(r'export_teams/$',
            self.admin_site.admin_view(self.export_teams),
            name='usermanagement_export_onsite_teams')
        ]
        return custom_urls + urls
    

class OnlineTeamAdmin(TeamAdmin):

    change_list_template = 'change_list_online_team.html'
    export_template = 'online_export.html'
    form = OnlineTeamForm

    def get_urls(self):
        urls = super(OnlineTeamAdmin, self).get_urls()
        custom_urls = [
            url(r'export_teams/$',
            self.admin_site.admin_view(self.export_teams),
            name='usermanagement_export_online_teams')
        ]
        return custom_urls + urls

class ContestantAdmin(admin.ModelAdmin):
    list_display = ['show_name', 'show_team', 'show_institution']

    def show_team(self, obj):
        return obj.team.name
    show_team.short_description = "team"

    def show_institution(self, obj):
        return obj.team.institution
    show_institution.short_description = "institution"

    def show_name(self, obj):
        return str(obj)
    show_name.short_description = 'name'

class OnsiteContestantAdmin(ContestantAdmin):
    class Meta:
        model = OnsiteContestant

class OnlineContestantAdmin(ContestantAdmin):
    class Meta:
        model = OnlineContestant

class MailMessageAdmin(admin.ModelAdmin):
    change_list_template = "change_list_mailmessage.html"
    send_custom_template = "send_custom_email.html"

    form = MailMessageForm

    def get_urls(self):
        urls = super(MailMessageAdmin, self).get_urls()
        custom_urls = [
            url(r'send_custom_emails/$',
            self.admin_site.admin_view(self.send_custom_emails),
            name='usermanagement_send_custom_emails')
        ]
        # Always add customs first to avoid problems
        return custom_urls + urls

    def send_custom_emails(self, request):
        context = {
            'title': ('Send Custom Emails'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }
        if request.method == 'POST':
            send_form = SendCustomEmailForm(request.POST)
            if send_form.is_valid():
                # raise Exception(self.__class__)
                return send_form.save()
        else:
            send_form = SendCustomEmailForm()
        context['form'] = send_form
        context['adminform'] = helpers.AdminForm(send_form,
                                                 list([(None, {'fields': send_form.base_fields})]),
                                                 {})

        return render(request, self.send_custom_template, context)


    class Meta:
        model = MailMessage


admin.site.register(OnsiteTeam, OnsiteTeamAdmin)
admin.site.register(OnlineTeam, OnlineTeamAdmin)
admin.site.register(OnlineContestant, OnlineContestantAdmin)
admin.site.register(OnsiteContestant, OnsiteContestantAdmin)
admin.site.register(Country)
admin.site.register(MailMessage, MailMessageAdmin)