from django.db import models

class Hotel(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    total_rooms = models.IntegerField()

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"

class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.customer_name} - {self.room}"

    def save(self, *args, **kwargs):
        # Mark room as unavailable when booking is created
        if not self.pk:  # Check if this is a new booking
            if not self.room.is_available:
                raise ValueError("Room is already booked.")
            self.room.is_available = False
            self.room.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Mark room as available when booking is canceled
        self.room.is_available = True
        self.room.save()
        super().delete(*args, **kwargs)