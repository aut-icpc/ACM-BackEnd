# Generated by Django 2.2.4 on 2019-08-28 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0002_auto_20190828_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acm',
            name='final_ranking_online',
            field=models.CharField(max_length=550),
        ),
        migrations.AlterField(
            model_name='acm',
            name='final_ranking_onsite',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='acm',
            name='judge_solution',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='acm',
            name='problems',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='acm',
            name='test_data',
            field=models.CharField(max_length=50),
        ),
    ]