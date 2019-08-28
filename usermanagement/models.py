from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

# EDU_LEVEL_CHOICES = (
#     'BSc',
#     'MSc',
#     "PhD"
# )

# GENDER_CHOICES = (
#     'male',
#     'female'
# )

# class Team(models.Model):
#     name = models.CharField(max_length=255)


# class Contestant(models.Model):
#     edu_level = models.CharField(max_length=3, choices=EDU_LEVEL_CHOICES)
#     email = models.CharField(max_length=255)
#     first_name = models.CharField(max_length=255)
#     gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
#     last_name = models.CharField(max_length=255)

#     phone_regex = RegexValidator(regex="09[0-9]{9}", message="Phone number must be entered correctly.")
#     phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True)

    
