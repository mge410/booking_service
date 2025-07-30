from django.contrib import admin
from hotels.models import Room, Booking


@admin.register(Room)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "price",
        "created_at",
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "start_date",
        "end_date",
    )
