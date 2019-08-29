# Generated by Django 2.2.4 on 2019-08-28 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ACM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('problems', models.CharField(max_length=20)),
                ('final_ranking_onsite', models.CharField(max_length=20)),
                ('final_ranking_online', models.CharField(max_length=20)),
                ('test_data', models.CharField(max_length=20)),
                ('judge_solution', models.CharField(max_length=20)),
            ],
        ),
    ]