from django.db import models

# Create your models here.

class Appointment(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    preferred_date = models.DateField(verbose_name="Preferred Date")
    preferred_time = models.TimeField(verbose_name="Preferred Time")
    vet = models.CharField(max_length=100, verbose_name="Vet Name")

    def __str__(self):
        return f"{self.name} appointment with {self.vet} on {self.preferred_date} at {self.preferred_time}"
