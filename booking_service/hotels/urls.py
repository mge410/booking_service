from rest_framework import routers
from django.urls import path, include
from hotels.views import RoomViewSet, BookingViewSet

router = routers.SimpleRouter()
router.register("room", RoomViewSet)
router.register("booking", BookingViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/", include(router.urls)),
]
