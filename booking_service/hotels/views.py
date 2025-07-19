from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers
from hotels.models import Room, Booking
from hotels.serializers import RoomSerializer, BookingSerializer


class RoomViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({"id": instance.id}, status=status.HTTP_201_CREATED)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)


class BookingViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        room_id = self.request.query_params.get('room') or self.request.query_params.get('room_id')

        if not room_id:
            raise serializers.ValidationError("Room parameter (room or room_id) is required")

        try:
            room_id = int(room_id)
        except (TypeError, ValueError):
            raise serializers.ValidationError("Room ID must be a valid integer")

        return queryset.filter(room_id=room_id)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({"id": instance.id}, status=status.HTTP_201_CREATED)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)
