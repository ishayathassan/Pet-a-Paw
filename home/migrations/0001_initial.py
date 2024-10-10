# Generated by Django 5.0.4 on 2024-05-03 20:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_num', models.CharField(max_length=11)),
                ('dob', models.DateField()),
                ('street', models.CharField(max_length=100)),
                ('house_no', models.CharField(max_length=20)),
                ('area', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='user_images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
