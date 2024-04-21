from django.shortcuts import HttpResponse


# Create your views here.
def home(request):
    return HttpResponse('<h1>Vet Home</h1>')
