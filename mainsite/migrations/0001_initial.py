# Generated by Django 2.2.3 on 2019-09-23 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Countdown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stopTime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeLineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateText', models.TextField()),
                ('style', models.TextField()),
                ('dateInnerStyle', models.TextField()),
                ('title', models.TextField()),
                ('innerHTML', models.TextField()),
            ],
        ),
    ]
