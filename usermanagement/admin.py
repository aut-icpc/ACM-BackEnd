from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    OnlineTeam,
    OnsiteTeam,
    OnlineContestant,
    OnsiteContestant,
    Country
)

# Register your models here.

class TeamForm(forms.ModelForm): 
    def clean(self):
        contestant = self.cleaned_data.get('contestant')
        if contestant.count() > 3:
            raise ValidationError("Too many contestants in one team")
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

class OnlineTeamAdmin(admin.ModelAdmin):
    form = OnlineTeamForm

class OnsiteTeamAdmin(admin.ModelAdmin):
    form = OnsiteTeamForm

admin.site.register(OnsiteTeam, OnsiteTeamAdmin)
admin.site.register(OnlineTeam, OnlineTeamAdmin)
admin.site.register(OnlineContestant)
admin.site.register(OnsiteContestant)
admin.site.register(Country)