from django.db import models
from django.contrib.postgres import fields
from django.core.validators import RegexValidator
from django.conf import settings
from .utils import send_mail

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


class MailMessage(models.Model):
    paid_subject = models.TextField(default='Paid')
    reserved_subject = models.TextField(default="Reserved registration beforehand")
    pending_subject = models.TextField(default="Pending")
    approved_subject = models.TextField(default="Approved for participation")
    denied_subject = models.TextField(default="Denied Participation")

    paid_content = models.TextField(default="")
    reserved_content = models.TextField(default="")
    pending_content = models.TextField(default="")
    approved_content = models.TextField(default="")
    denied_content = models.TextField(default="")

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
    name = models.CharField(max_length=255, unique=True)
    institution = models.CharField(max_length=255)

    email = ""

    def __str__(self):
        return self.name

        
    
class OnlineTeam(Team):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=ONLINE_TEAM_STATUS_CHOICES, default='APPROVED')

    def save(self, *args, **kwargs):
        mailmessage = MailMessage.load()
        #Online team is accepted by default, unless something changes. 
        send_mail(self.name, self.email, mailmessage.approved_subject, mailmessage.approved_content)
        super(OnlineTeam, self).save(*args, **kwargs)


class OnsiteTeam(Team):
    status = models.CharField(max_length=50, choices=ONSITE_TEAM_STATUS_CHOICES, default="PENDING")

    def save(self, *args, **kwargs):

        mailmessage = MailMessage.load()
        email = self.email
        name = self.name

        if self.status == 'PENDING':
            send_mail(name, email, mailmessage.pending_subject, mailmessage.pending_content)
        elif self.status == 'RESERVED':
            send_mail(name, email, mailmessage.reserved_subject, mailmessage.reserved_content)
        elif self.status == 'APPROVED':
            send_mail(name, email, mailmessage.approved_subject, mailmessage.approved_content)
        elif self.status == 'PAID':
            send_mail(name, email, mailmessage.paid_subject, mailmessage.paid_content)
        elif self.status == ' REJECTED':
            send_mail(name, email, mailmessage.denied_subject, mailmessage.denied_content)

        super(OnsiteTeam, self).save(*args, **kwargs)





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

    # class Meta:
    #     abstract = True


class OnlineContestant(Contestant):
    pass


class OnsiteContestant(Contestant):
    shirt_size = models.CharField(max_length=20, choices=T_SHIRT_SIZE_CHOICES, default='M')
