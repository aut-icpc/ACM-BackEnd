from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Team,
    OnlineContestant,
    OnsiteContestant,
    Country
)

# Register your models here.

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
    
    def clean(self):
        contestant = self.cleaned_data.get('contestant')
        if contestant.count() > 3:
            raise ValidationError("Too many contestants in one team")
        return self.cleaned_data

class TeamAdmin(admin.ModelAdmin):
    form = TeamForm

admin.site.register(Team, TeamAdmin)
admin.site.register(OnlineContestant)
admin.site.register(OnsiteContestant)
admin.site.register(Country)