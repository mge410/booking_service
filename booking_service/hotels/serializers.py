from rest_framework import serializers
from hotels.models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            "id",
            "description",
            "price",
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "room",
            "start_date",
            "end_date",
        ]

    def validate(self, data: dict) -> dict:
        if data["end_date"] <= data["start_date"]:
            raise serializers.ValidationError("End date must be after start date")

        if Booking.objects.filter(
            room=data["room"],
            start_date__lt=data["end_date"],
            end_date__gt=data["start_date"],
        ).exists():
            raise serializers.ValidationError(
                "This room is already booked for the selected dates"
            )

        return data
