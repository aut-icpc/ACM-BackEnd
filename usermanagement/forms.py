from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import (
    OnsiteTeam,
    OnlineTeam,
    MailMessage,
    ONSITE_TEAM_STATUS_CHOICES
)
from django.http import HttpResponseServerError, FileResponse, HttpResponseBadRequest, HttpResponse
from .utils import (
    export_teams, 
    export_contestants,
    team_json_to_sv_file_response
) 

from .tasks import enqueue_mail

import json
import io


class TeamForm(forms.ModelForm): 

    do_email = forms.BooleanField(initial=False, label="Send new Email?", required=False, 
    help_text="""If you don't check this field when finalizing a team, It'll not generate a user/pass for them.""")

    def clean(self):
        contestant = self.cleaned_data.get('contestant')
        try:
            if contestant.count() > 3:
                raise ValidationError("Too many contestants in one team")
        except AttributeError as ex:
            print(ex)
            print("Adding teams through admin is kinda bad practice, kinda.")
        return self.cleaned_data
    
    def save(self, commit=True):
        instance = super(TeamForm, self).save(commit=False)
        instance.sendNewMail = ('status' in self.changed_data) and self.cleaned_data['do_email']
        if commit:
            instance.save()
        return instance

class OnlineTeamForm(TeamForm):
    list_display = ('name', 'country', 'institution')
    class Meta:
        model = OnlineTeam
        fields = '__all__'

class OnsiteTeamForm(TeamForm):
    class Meta:
        model = OnsiteTeam
        fields = '__all__'

class MailMessageForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = '__all__'

EXPORT_CHOICES = (
    ('JSON', 'JSON'),
    ('CSV', 'CSV'),
    ('TSV', 'TSV')
)

FORMAT_CHOICES = (
    ('TEAM', 'Team-based'),
    ('CONTESTANT', 'Contestant-Based')
)

JUDGE_CHOICES = (
    ('ACCOUNTS', 'Accounts'),
    ('TEAMS', 'Teams')
)

class ExportTeamForm(forms.Form):
    is_for_judge = forms.BooleanField(required=False)
    judge_export_type = forms.ChoiceField(choices=JUDGE_CHOICES)

    export_type = forms.ChoiceField(choices=EXPORT_CHOICES)
    format_type = forms.ChoiceField(choices=FORMAT_CHOICES)
    is_finalized = forms.BooleanField(required=False, label="Only finalized teams?")

    def save(self, adminType=None):
        exp_type = self.cleaned_data['export_type']
        format_type = self.cleaned_data['format_type']
        is_finalized = self.cleaned_data['is_finalized']
        is_for_judge = self.cleaned_data['is_for_judge']
        judge_export_type = self.cleaned_data['judge_export_type']
        file_name = adminType.__name__[:-5] + 's-' + format_type + '-' + datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

        if format_type == 'TEAM':
            teams_json = export_teams(adminType, is_finalized)
        elif format_type == 'CONTESTANT':
            if is_for_judge:
                return HttpResponseBadRequest('Judge can only see team-based export.')
            teams_json = export_contestants(adminType, is_finalized)

        if exp_type == 'JSON':
            file_name += ".json"
            json_bytes = json.dumps(teams_json).encode('utf-8')
            json_bytesIO = io.BytesIO(json_bytes)
            response = FileResponse(json_bytesIO)
            response['Content-Disposition'] = 'attachment; filename= %s' %file_name
            return response
           
        elif exp_type == 'CSV':
            file_name += '.csv'
            return team_json_to_sv_file_response(teams_json, file_name, ',', is_for_judge, judge_export_type)
        
        elif exp_type == 'TSV':
            file_name += '.tsv'
            return team_json_to_sv_file_response(teams_json, file_name, '\t', is_for_judge, judge_export_type)


        return HttpResponseBadRequest

class SendCustomEmailForm(forms.Form):
    is_onsite = forms.BooleanField(help_text="Check for onsite teams, uncheck for online.")
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(choices=ONSITE_TEAM_STATUS_CHOICES)

    def save(self):
        is_onsite = self.cleaned_data['is_onsite']
        subject = self.cleaned_data['subject']
        content = self.cleaned_data['content']
        status = self.cleaned_data['status']

        if is_onsite:
            team_model = OnsiteTeam
        else:
            team_model = OnlineTeam
            if status == "RESERVED" or status == "APPROVED":
                return HttpResponseBadRequest("Online teams can't be reserved or approved!")
        
        teams = team_model.objects.filter(status=status)
        for team in teams:
            enqueue_mail(team, subject, content)
        
        return HttpResponse("Emails sent successfully!")


