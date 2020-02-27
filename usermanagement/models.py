from django.db import models
from django.contrib.postgres import fields
from django.core.validators import RegexValidator, EmailValidator
from django.conf import settings
from .utils import generate_email_json, send_mail
import uuid

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
    ('PENDING', 'Pending Approval'),
    ('APPROVED', 'Approved for payment'),
    ('REJECTED', 'Denied Participation')
)

ONSITE_TEAM_STATUS_CHOICES = (
    ('PAID', 'Finalized Registration'),
    ('RESERVED', 'Reserved registration beforehand') ) + TEAM_STATUS_CHOICES

#TODO: This should be changed as online teams have no payment process.
ONLINE_TEAM_STATUS_CHOICES = () + TEAM_STATUS_CHOICES


class Country(models.Model):
    name = models.CharField(max_length=255)
    flag = models.ImageField()

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class MailMessage(models.Model):
    paid_subject = models.TextField(default='Paid')
    reserved_subject = models.TextField(default="Reserved registration beforehand")
    pending_subject = models.TextField(default="Pending")
    approved_subject = models.TextField(default="Approved for participation")
    denied_subject = models.TextField(default="Denied Participation")
    online_subject = models.TextField(default="")

    paid_content = models.TextField(default="")
    reserved_content = models.TextField(default="")
    pending_content = models.TextField(default="")
    approved_content = models.TextField(default="")
    denied_content = models.TextField(default="")
    online_content = models.TextField(default="")

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        super(MailMessage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass


class Team(models.Model):
    name = models.CharField(max_length=25, unique=True)
    institution = models.CharField(max_length=50)

    email = ""

    def __str__(self):
        return self.name

    def get_email(self):
        return self.email or self.contestants.get(is_primary=True).email
    
    def send_team_mail(self, password=None, override_status=None):
        status = override_status or self.status
        mailmessage = MailMessage.load()

        #TODO: Add sending password by default!
        
        if self.sendNewMail:
            if status == 'PENDING':
                send_mail(self.name, self.get_email(), mailmessage.pending_subject, mailmessage.pending_content)
            elif status == 'APPROVED':
                send_mail(self.name, self.get_email(), mailmessage.online_subject, mailmessage.online_content)



class OnlineTeam(Team):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ONLINE_TEAM_STATUS_CHOICES, default='APPROVED')
    password = models.CharField(max_length=20, default="")

    # Online team is accepted by default, unless something changes. 
    def save(self, *args, **kwargs):

        self.password = uuid.uuid4().hex[:8]
        self.send_team_mail(override_status='APPROVED')
        super(OnlineTeam, self).save(*args, **kwargs)



class OnsiteTeam(Team):
    status = models.CharField(max_length=50, choices=ONSITE_TEAM_STATUS_CHOICES, default="PENDING")

    def save(self, *args, **kwargs):
       
        self.send_team_mail()
        super(OnsiteTeam, self).save(*args, **kwargs)        


class Contestant(models.Model):
    phone_validator = RegexValidator(regex=r"^(\+98|0)?9\d{9}$", message="Phone number must be entered correctly.")
    email_validator = EmailValidator(message="Email must be entered correctly.")

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    edu_level = models.CharField(max_length=3, choices=EDU_LEVEL_CHOICES, default='BSC')
    student_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100, unique=True, validators=[email_validator])
    phone_number = models.CharField(validators=[phone_validator], blank=True, max_length=20, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='contestants')
    is_primary = models.BooleanField(default=False)
 
    def __str__(self):
        return self.first_name + " " + self.last_name

class OnlineContestant(Contestant):
    pass

class OnsiteContestant(Contestant):
    shirt_size = models.CharField(max_length=20, choices=T_SHIRT_SIZE_CHOICES, default='M')
