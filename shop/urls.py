from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_view, name='shop'),
    path('product/<int:id>/', views.product_view, name='single_product'),
    path('cart/',views.cart_view,name='cart'),
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
    path('update_cart/', views.update_cart, name='update_cart'),\
    path('submit_review/<int:id>/', views.submit_review, name='submit_review'),
]
