from django.shortcuts import render, redirect
from .models import Appointment
from django.contrib import messages

# Create your views here.
def vet_view(request):
    if request.method == 'POST':
        # Extracting data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')
        preferred_date = request.POST.get('date')
        preferred_time = request.POST.get('time')
        vet = request.POST.get('vet')
        
        # Creating an Appointment instance and saving it to the database
        appointment = Appointment(
            name=name,
            email=email,
            phone_number=phone_number,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            vet=vet
        )
        appointment.save()
        
        # After saving, you can redirect to a new URL or show a success message
        messages.success(request, 'Appointment scheduled successfully!')
        return render(request, 'vet/vet_home.html') # Replace 'success_url' with the name of the URL where users should be redirected

    # If a GET (or any other method) we'll create a blank form
    else:
        return render(request, 'vet/vet_home.html')
    
