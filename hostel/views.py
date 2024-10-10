from django.shortcuts import render, redirect
from .models import HostelRooms, BookHostel


# Create your views here.

def hostel_view(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        room_num = request.POST.get('room')

        # Room Availability Check
        room = HostelRooms.objects.get(room_num=room_num)
        # if not room.is_occupied:
        BookHostel.objects.create(start_date=date, time=time, room_num=room)
        # room.is_occupied = True
        # room.save()
        # return redirect('hostel')
        # else:
        #     # Room is not available
        #     # messages.error(request, 'Room is not available!')
        #     return redirect('hostel')  # Redirect back to the booking page
    return render(request, 'hostel/hostel.html')
