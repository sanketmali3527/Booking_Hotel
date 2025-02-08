from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Hotel, Room, Booking
from .forms import BookingForm

def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotel/hotel_list.html', {'hotels': hotels})

def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel, is_available=True)
    return render(request, 'hotel/room_list.html', {'hotel': hotel, 'rooms': rooms})

def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.hotel = room.hotel
            try:
                booking.save()
                messages.success(request, 'Room booked successfully!')
                return redirect('booking_confirmation', booking_id=booking.id)
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = BookingForm()
    return render(request, 'hotel/book_room.html', {'form': form, 'room': room})

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'hotel/booking_confirmation.html', {'booking': booking})