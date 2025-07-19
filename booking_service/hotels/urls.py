from rest_framework import routers
from django.urls import path, include
from hotels.views import RoomViewSet

router = routers.SimpleRouter()
router.register("room", RoomViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
