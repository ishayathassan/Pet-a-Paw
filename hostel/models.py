from django.db import models


# Create your models here.
class HostelRooms(models.Model):
    room_num = models.CharField(primary_key=True, max_length=20)
    is_occupied = models.BooleanField(default=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    check_in = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"Room {self.room_num}"


class BookHostel(models.Model):
    start_date = models.DateField()
    time = models.CharField(max_length=100)
    room_num = models.ForeignKey(HostelRooms, on_delete=models.CASCADE)
    end_date = models.DateField(null=True)

    def __str__(self):
        return f"Booking for Room {self.room_num}"
