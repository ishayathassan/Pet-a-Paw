# Generated by Django 5.0.4 on 2024-05-03 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Full Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Phone Number')),
                ('preferred_date', models.DateField(verbose_name='Preferred Date')),
                ('preferred_time', models.TimeField(verbose_name='Preferred Time')),
                ('vet', models.CharField(max_length=100, verbose_name='Vet Name')),
            ],
        ),
    ]
