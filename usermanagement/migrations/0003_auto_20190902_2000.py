# Generated by Django 2.2.3 on 2019-09-02 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0002_auto_20190902_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onsiteteam',
            name='team_ptr',
        ),
        migrations.DeleteModel(
            name='OnlineTeam',
        ),
        migrations.DeleteModel(
            name='OnsiteTeam',
        ),
    ]
