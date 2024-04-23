from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_view, name='shop'),
    path('product/<int:id>/', views.product_view, name='single_product'),
]
