from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, default="")
    price = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    details = models.TextField()

    def __str__(self):
        return self.name
