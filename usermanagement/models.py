from django.db import models
from django.contrib.postgres import fields
from django.core.validators import RegexValidator

# Create your models here.

EDU_LEVEL_CHOICES = (
    ('bsc', 'BSc'),
    ('msc', 'MSc'),
    ("phd", 'PhD')
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

T_SHIRT_SIZE = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'X-Large'),
    ('2XL', '2X-Large'),
    ('3XL', '3X-Large')
)

class Country(models.Model):
    name = models.CharField(max_length=255)
    flag = models.ImageField()
    class Meta:
        verbose_name_plural = 'Countries'

class Team(models.Model):
    name = models.CharField(max_length=255)
    is_onsite = models.BooleanField()
    

class Contestant(models.Model):
    edu_level = models.CharField(max_length=3, choices=EDU_LEVEL_CHOICES)
    email = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    last_name = models.CharField(max_length=255)

    phone_regex = RegexValidator(regex="09[0-9]{9}", message="Phone number must be entered correctly.")
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True)

    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class OnlineContestant(Contestant):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

class OnsiteContestant(Contestant):
    shirt_size = models.CharField(max_length=20, choices=T_SHIRT_SIZE)
    