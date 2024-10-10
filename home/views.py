from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from shop.models import OrderDetails, OrderedProducts
from django.contrib import messages

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


@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    orders = OrderDetails.objects.filter(user_id=request.user).prefetch_related('orderedproducts_set__product_id')[:5]

    context = {
        'user_profile': user_profile,
        'orders': orders,
    }
    return render(request, 'home/profile.html', context)
@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.name = request.POST.get('editName', user_profile.name)  # Default to existing if not provided
            user_profile.email = request.POST.get('editEmail', user_profile.email)
            user_profile.phone_num = request.POST.get('editPhone', user_profile.phone_num)
            user_profile.street = request.POST.get('editStreet', user_profile.street)
            user_profile.house_no = request.POST.get('editHouse', user_profile.house_no)
            user_profile.area = request.POST.get('editArea', user_profile.area)

            # Assuming there might be additional fields such as an image
            if 'editImage' in request.FILES:
                user_profile.image = request.FILES['editImage']

            user_profile.save()
            messages.success(request, 'Your profile was updated successfully.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'Profile not found.')
        except Exception as e:
            messages.error(request, 'Error updating profile: {}'.format(e))
        return redirect('/profile')
    else:
        # If not POST, redirect back to the profile page or to a safe page
        messages.error(request, 'Invalid request method.')
        return redirect('/profile')
    

def order_history_view(request):
    user_id = request.user.id
    orders = OrderDetails.objects.filter(user_id=user_id)[:5]
    context = {'orders': orders}
    return render(request, 'home/profile.html', context)