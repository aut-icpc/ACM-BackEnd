# Generated by Django 2.2.3 on 2019-08-24 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0002_countdown'),
    ]

    operations = [
        migrations.RenameField(
            model_name='countdown',
            old_name='startTime',
            new_name='stopTime',
        ),
    ]