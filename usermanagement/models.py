from django.db import models
from django.contrib.postgres import fields
from django.core.validators import RegexValidator

# Create your models here.

EDU_LEVEL_CHOICES = (
    ('BSC', 'BSc'),
    ('MSC', 'MSc'),
    ("PHD", 'PhD')
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
)

T_SHIRT_SIZE_CHOICES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'X-Large'),
    ('2XL', '2X-Large'),
    ('3XL', '3X-Large')
)

TEAM_STATUS_CHOICES = (
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved for participation'),
    ('REJECTED', 'Denied Participation')
)

ONSITE_TEAM_STATUS_CHOICES = (
    ('PAID', 'Paid'),
    ('RESERVED', 'Reserved registration beforehand') ) + TEAM_STATUS_CHOICES

ONLINE_TEAM_STATUS_CHOICES = () + TEAM_STATUS_CHOICES

class Country(models.Model):
    name = models.CharField(max_length=255)
    flag = models.ImageField()
    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    institution = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class OnlineTeam(Team):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ONLINE_TEAM_STATUS_CHOICES, default='PENDING')

class OnsiteTeam(Team):
    status = models.CharField(max_length=50, choices=ONSITE_TEAM_STATUS_CHOICES, default="PENDING")


class Contestant(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    edu_level = models.CharField(max_length=3, choices=EDU_LEVEL_CHOICES, default='BSC')
    student_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='contestants')


    def __str__(self):
        return self.first_name + " " + self.last_name


class OnlineContestant(Contestant):
    pass
    

class OnsiteContestant(Contestant):
    shirt_size = models.CharField(max_length=20, choices=T_SHIRT_SIZE_CHOICES, default='M')
    
