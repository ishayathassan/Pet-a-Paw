from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_num = models.CharField(max_length=11)
    dob = models.DateField()
    street = models.CharField(max_length=100)
    house_no = models.CharField(max_length=20)
    area = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username
