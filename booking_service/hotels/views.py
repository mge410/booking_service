from rest_framework.request import Request

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from hotels.models import Room
from hotels.serializers import RoomSerializer
from rest_framework import status
from rest_framework import filters


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
