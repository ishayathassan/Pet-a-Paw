from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=50)
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, default="")
    price = models.FloatField(default=0)
    stock = models.IntegerField(default=0)
    details = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if the product is being created (not already in the database)
        if not self.id:
            # Get the maximum ID from existing products
            max_id = Product.objects.aggregate(models.Max('id'))['id__max'] or 0
            # Set the ID of the new product to one greater than the maximum ID
            self.id = max_id + 1
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
