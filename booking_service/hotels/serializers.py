from rest_framework import serializers
from hotels.models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            Room.id.field.name,
            Room.description.field.name,
            Room.price.field.name,
        ]

    def create(self, validated_data: dict) -> Room:
        return Room.objects.create(**validated_data)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            Room.id.field.name,
            Booking.room.field.name,
            Booking.start_date.field.name,
            Booking.end_date.field.name,
        ]

    def validate(self, data: dict) -> dict:
        if data["end_date"] <= data["start_date"]:
            raise serializers.ValidationError("End date must be after start date")
        return data
