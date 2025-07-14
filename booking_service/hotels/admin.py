from django.contrib import admin
import hotels.models


@admin.register(hotels.models.Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        hotels.models.Hotel.title.field.name,
        hotels.models.Hotel.text.field.name,
    )


@admin.register(hotels.models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        hotels.models.Booking.hotel.field.name,
        hotels.models.Booking.start_date.field.name,
        hotels.models.Booking.end_date.field.name,
    )
