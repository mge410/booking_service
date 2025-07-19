from rest_framework import serializers
from hotels.models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            Room.description.field.name,
            Room.price.field.name,
        ]

    def create(self, validated_data: dict) -> Room:
        return Room.objects.create(**validated_data)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            Booking.room.field.name,
            Booking.start_date.field.name,
            Booking.end_date.field.name,
        ]

    def validate(self, data: dict) -> dict:
        if data["end_date"] <= data["start_date"]:
            raise serializers.ValidationError("End date must be after start date")
        return data


class BookingCreateSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    date_start = serializers.DateField()
    date_end = serializers.DateField()

    def validate(self, data: dict) -> dict:
        try:
            if data["date_end"] <= data["date_start"]:
                raise serializers.ValidationError("End date must be after start date")
        except KeyError:
            pass
        return data
