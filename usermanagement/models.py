from django.db import models
from django.contrib.postgres import fields
from django.core.validators import RegexValidator, EmailValidator
from django.conf import settings
from .utils import generate_email_json, send_mail
import uuid
# from usermanagement.rabbitmq.sender import Sender

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

# sender = None

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

class OnlineTeam(Team):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ONLINE_TEAM_STATUS_CHOICES, default='APPROVED')
    password = models.CharField(max_length=20, default="")

    def save(self, *args, **kwargs):
        mailmessage = MailMessage.load()
        # Online team is accepted by default, unless something changes. 
        self.password = uuid.uuid4().hex[:8]
        super(OnlineTeam, self).save(*args, **kwargs)
        email = self.get_email()


        # mail_json = generate_email_json(self.name, email, mailmessage.online_subject, mailmessage.online_content, self.password)
        # if not sender:
        #     sender = Sender()

        send_mail(self.name, email, mailmessage.online_subject, mailmessage.online_content, self.password)
        
        # sender.publish_mail(mail_json)


class OnsiteTeam(Team):
    status = models.CharField(max_length=50, choices=ONSITE_TEAM_STATUS_CHOICES, default="PENDING")

    def save(self, *args, **kwargs):

        mailmessage = MailMessage.load()
        email = self.get_email()
        name = self.name

        super(OnsiteTeam, self).save(*args, **kwargs)

        # if not sender:
        #     sender = Sender()

        if self.status == 'PENDING':
            send_mail(name, email, mailmessage.pending_subject, mailmessage.pending_content)
            
        #    mail_json = generate_email_json(name, email, mailmessage.pending_subject, mailmessage.pending_content)
        #    sender.publish_mail(mail_json)
        # elif self.status == 'RESERVED':
        #     mail_json = generate_email_json(name, email, mailmessage.reserved_subject, mailmessage.reserved_content)
        #     sender.publish_mail(mail_json)
        # elif self.status == 'APPROVED':
        #     mail_json = generate_email_json(name, email, mailmessage.approved_subject, mailmessage.approved_content)
        #     sender.publish_mail(mail_json)
        # elif self.status == 'PAID':
        #     mail_json = generate_email_json(name, email, mailmessage.paid_subject, mailmessage.paid_content)
        #     sender.publish_mail(mail_json)
        # elif self.status == ' REJECTED':
        #     mail_json = generate_email_json(name, email, mailmessage.denied_subject, mailmessage.denied_content)
        #     sender.publish_mail(mail_json)


class Contestant(models.Model):
    phone_validator = RegexValidator(regex=r"^(\+98|0)?9\d{9}$", message="Phone number must be entered correctly.")
    email_validator = EmailValidator(message="Email must be entered correctly.")

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    edu_level = models.CharField(max_length=3, choices=EDU_LEVEL_CHOICES, default='BSC')
    student_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100, unique=True, validators=[email_validator])
    phone_number = models.CharField(validators=[phone_validator], blank=True, max_length=20)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='contestants')
    is_primary = models.BooleanField(default=False)
 
    def __str__(self):
        return self.first_name + " " + self.last_name

class OnlineContestant(Contestant):
    pass

class OnsiteContestant(Contestant):
    shirt_size = models.CharField(max_length=20, choices=T_SHIRT_SIZE_CHOICES, default='M')
