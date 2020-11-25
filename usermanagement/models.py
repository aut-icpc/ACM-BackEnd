import uuid
from django.db import models
from django.contrib.postgres import fields
from django.core.validators import RegexValidator, EmailValidator
from django.conf import settings
from usermanagement.tasks import enqueue_mail
from usermanagement.apps import UsermanagementConfig as config
from contests.models import CurrentContest


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
    ('REJECTED', 'Denied Participation'),
    ('FINALIZED', 'Finalized Registration'),
)

ONSITE_TEAM_STATUS_CHOICES = (
    ('APPROVED', 'Approved for payment'),
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
    pending_subject = models.TextField(default="Pending")
    pending_content = models.TextField(default="")

    rejected_subject = models.TextField(default="Rejected")
    rejected_content = models.TextField(default="")

    finalized_subject = models.TextField(default="Finalized")
    finalized_content = models.TextField(default="")

    approved_subject = models.TextField(default="Approved for participation")
    approved_content = models.TextField(default="")

    reserved_subject = models.TextField(default="Reserved registration beforehand")
    reserved_content = models.TextField(default="")

    online_subject = models.TextField(default="Online Contest Registration")
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
    user = models.CharField(max_length=10, unique=True, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)

    email = ""
    emails = []

    def __str__(self):
        return self.name

    def get_email(self):
        return self.email or self.contestants.get(is_primary=True).email

    def get_emails(self):
        return self.emails or list(self.contestants.values_list('email', flat=True))

    def get_user_pass_and_increment_base(self, self_type):
        currentC = CurrentContest.load()
        if self_type == 'online':
            number = currentC.online_team_starting_user_count
            currentC.online_team_starting_user_count += 1
        elif self_type == 'onsite':
            number = currentC.onsite_team_starting_user_count
            currentC.onsite_team_starting_user_count += 1
        currentC.save()
        user = 'team-' + str(number).zfill(3)
        password = uuid.uuid4().hex[:8]
        return user, password


class OnlineTeam(Team):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ONLINE_TEAM_STATUS_CHOICES, default='PENDING')

    def save(self, *args, **kwargs):
        try:
            if self.sendNewMail:
                if self.status == 'FINALIZED' and self.user == None:
                    self.user, self.password = self.get_user_pass_and_increment_base('online')

                mailmessage = MailMessage.load()
                enqueue_mail(self, mailmessage.online_subject, mailmessage.online_content)
        except:
            pass
        super(OnlineTeam, self).save(*args, **kwargs)


class OnsiteTeam(Team):
    status = models.CharField(max_length=50, choices=ONSITE_TEAM_STATUS_CHOICES, default="PENDING")
    is_high = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            if self.sendNewMail:
                mailmessage = MailMessage.load()
                if self.status == 'PENDING':
                    subject, content = mailmessage.pending_subject, mailmessage.pending_content
                elif self.status == 'RESERVED':
                    subject, content = mailmessage.reserved_subject, mailmessage.reserved_content
                elif self.status == 'APPROVED':
                    subject, content = mailmessage.approved_subject, mailmessage.approved_content
                elif self.status == 'FINALIZED':
                    subject, content = mailmessage.finalized_subject, mailmessage.finalized_content
                    if self.user == None:
                        self.user, self.password = self.get_user_pass_and_increment_base('onsite')
                elif self.status == 'REJECTED':
                    subject, content = mailmessage.rejected_subject, mailmessage.rejected_content
                
                enqueue_mail(self, subject, content)
        except:
            pass
        
        super(OnsiteTeam, self).save(*args, **kwargs)

       

class Contestant(models.Model):
    phone_validator = RegexValidator(regex=r"^(\+98|0)?9\d{9}$", message="Phone number must be entered correctly.")
    email_validator = EmailValidator(message="Email must be entered correctly.")
    student_number_validator = RegexValidator(regex=r"\d{1,20}")

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    edu_level = models.CharField(max_length=3, choices=EDU_LEVEL_CHOICES, default='BSC')
    student_number = models.CharField(validators=[student_number_validator], max_length=20)
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
