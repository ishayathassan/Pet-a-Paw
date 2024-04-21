from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, HttpResponse, redirect

from .forms import RegisterForm, LoginForm
from .models import UserProfile


# Create your views here.

def home_view(request):
    return render(request, 'home/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone_num=form.cleaned_data['phone_num'],
                dob=form.cleaned_data['dob'],
                street=form.cleaned_data['street'],
                house_no=form.cleaned_data['house_no'],
                area=form.cleaned_data['area']
            )
            login(request, user)
            return redirect('home')  # Redirect to home page after registration
    else:
        form = RegisterForm()
    return render(request, 'home/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
