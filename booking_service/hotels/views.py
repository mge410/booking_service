from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers
from hotels.models import Room, Booking
from hotels.serializers import RoomSerializer, BookingSerializer
from django.shortcuts import get_object_or_404


class BaseCreateDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({"id": instance.id}, status=status.HTTP_201_CREATED)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        return super().destroy(request, *args, **kwargs)


class RoomViewSet(BaseCreateDeleteViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = [
        Room.price.field.name,
        Room.created_at.field.name
    ]
    ordering = [f"-{Room.created_at.field.name}"]


class BookingViewSet(BaseCreateDeleteViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    ordering = [Booking.start_date.field.name]

    def get_queryset(self):
        queryset = super().get_queryset()
        room_id = self.request.query_params.get('room') or self.request.query_params.get('room_id')

        if not room_id:
            raise serializers.ValidationError("Room parameter (room or room_id) is required")

        try:
            get_object_or_404(Room, id=int(room_id))
            return queryset.filter(room_id=room_id)
        except ValueError:
            raise serializers.ValidationError(
                {"room": "Room ID must be a valid integer"}
            )
