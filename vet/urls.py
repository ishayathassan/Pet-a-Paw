from django.urls import path
from . import views

urlpatterns = [
    path('', views.vet_view, name='vet_home'),
]
