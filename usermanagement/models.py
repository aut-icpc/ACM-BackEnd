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
    ('PENDING', 'Pending Payment'),
    ('PAID', 'Paid'),
    ('APPROVED', 'Approved for participation'),
    ('REJECTED', 'Denied Participation'),
    ('RESERVED', 'Reserved registration beforehand')
)

class Country(models.Model):
    name = models.CharField(max_length=255)
    flag = models.ImageField()
    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_onsite = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=TEAM_STATUS_CHOICES, default='PENDING')
    institution = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Contestant(models.Model):
    # phone_regex = RegexValidator(regex="09[0-9]{9}", message="Phone number must be entered correctly.")

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    edu_level = models.CharField(max_length=3, choices=EDU_LEVEL_CHOICES, default='BSC')
    student_number = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    # phone_number = models.CharField(validators=[phone_regex], max_length=12, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = ["email", "phone_number"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class OnlineContestant(Contestant):
    pass
    

class OnsiteContestant(Contestant):
    shirt_size = models.CharField(max_length=20, choices=T_SHIRT_SIZE_CHOICES, default='M')
    
