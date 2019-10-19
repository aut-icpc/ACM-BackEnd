from django import forms
from django.core.exceptions import ValidationError
from .models import (
    OnsiteTeam,
    OnlineTeam,
)
from django.http import HttpResponseServerError, FileResponse
from .utils import (
    export_teams, 
    export_contestants,
    team_json_to_sv_file_response
) 
import json
import io


class TeamForm(forms.ModelForm): 
    def clean(self):
        contestant = self.cleaned_data.get('contestant')
        try:
            if contestant.count() > 3:
                raise ValidationError("Too many contestants in one team")
        except AttributeError as ex:
            print(ex)
            print("Adding teams through admin is kinda bad practice, kinda.")
        return self.cleaned_data

class OnlineTeamForm(TeamForm):
    list_display = ('name', 'country', 'institution')
    class Meta:
        model = OnlineTeam
        fields = '__all__'

class OnsiteTeamForm(TeamForm):
    class Meta:
        model = OnsiteTeam
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

class ExportTeamForm(forms.Form):
    export_type = forms.ChoiceField(choices=EXPORT_CHOICES)
    format_type = forms.ChoiceField(choices=FORMAT_CHOICES)

    def save(self, adminType=None):
        file_name = adminType.__name__[:-5]
        exp_type = self.cleaned_data['export_type']
        format_type = self.cleaned_data['format_type']

        if format_type == 'TEAM':
            teams_json = export_teams(adminType)
        elif format_type == 'CONTESTANT':
            teams_json = export_contestants(adminType)

        if exp_type == 'JSON':
            file_name += ".json"
            json_bytes = json.dumps(teams_json).encode('utf-8')
            json_bytesIO = io.BytesIO(json_bytes)
            response = FileResponse(json_bytesIO)
            response['Content-Disposition'] = 'attachment; filename= %s' %file_name
            return response
           
        elif exp_type == 'CSV':
            file_name += '.csv'
            return team_json_to_sv_file_response(teams_json, file_name, ',')
        
        elif exp_type == 'TSV':
            file_name += '.tsv'
            return team_json_to_sv_file_response(teams_json, file_name, '\t')


        return HttpResponseServerError

