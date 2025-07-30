from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import serializers
from rest_framework import viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from hotels.models import Room, Booking
from hotels.serializers import RoomSerializer, BookingSerializer


class BaseCreateDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    def create(self, request: Request, *args, **kwargs) -> Response:
        response = super().create(request, *args, **kwargs)
        return Response({"id": response.data["id"]}, status=response.status_code)


class RoomViewSet(BaseCreateDeleteViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]


class BookingViewSet(BaseCreateDeleteViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    ordering = ["start_date"]

    def list(self, request, *args, **kwargs):
        room_id = self.get_room_id_from_request(request)
        get_object_or_404(Room, id=room_id)  # Проверяем существование комнаты
        self.queryset = self.queryset.filter(room_id=room_id)
        return super().list(request, *args, **kwargs)

    @staticmethod
    def get_room_id_from_request(request):
        room_id = request.query_params.get("room")
        if not room_id:
            raise serializers.ValidationError("Room parameter room is required")

        try:
            return int(room_id)
        except ValueError:
            raise serializers.ValidationError(
                {"room": "Room ID must be a valid integer"}
            )
