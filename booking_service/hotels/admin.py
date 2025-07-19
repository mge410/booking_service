from django.contrib import admin
from hotels.models import Room, Booking


@admin.register(Room)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        Room.description.field.name,
        Room.price.field.name,
        Room.created_at.field.name,
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        Booking.room.field.name,
        Booking.start_date.field.name,
        Booking.end_date.field.name,
    )
