from django.contrib import admin
from .models import Product,Cart,OrderDetails, OrderedProducts,Review

# Register your models here.
admin.site.register(Product)

admin.site.register(Cart)

admin.site.register(OrderDetails)

admin.site.register(OrderedProducts)

admin.site.register(Review)
