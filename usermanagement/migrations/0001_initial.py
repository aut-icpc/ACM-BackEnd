# Generated by Django 2.2.3 on 2019-09-01 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=5)),
                ('edu_level', models.CharField(choices=[('BSC', 'BSc'), ('MSC', 'MSc'), ('PHD', 'PhD')], default='BSC', max_length=3)),
                ('student_number', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('flag', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='OnlineContestant',
            fields=[
                ('contestant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usermanagement.Contestant')),
            ],
            bases=('usermanagement.contestant',),
        ),
        migrations.CreateModel(
            name='OnsiteContestant',
            fields=[
                ('contestant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='usermanagement.Contestant')),
                ('shirt_size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'X-Large'), ('2XL', '2X-Large'), ('3XL', '3X-Large')], default='M', max_length=20)),
            ],
            bases=('usermanagement.contestant',),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('is_onsite', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('PENDING', 'Pending Payment'), ('PAID', 'Paid'), ('APPROVED', 'Approved for participation'), ('REJECTED', 'Denied Participation'), ('RESERVED', 'Reserved registration beforehand')], default='PENDING', max_length=50)),
                ('institution', models.CharField(max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement.Country')),
            ],
        ),
        migrations.AddField(
            model_name='contestant',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement.Team'),
        ),
    ]
