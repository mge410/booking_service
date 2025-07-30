import pytest
from rest_framework.test import APIClient
from datetime import date, timedelta

from hotels.models import Booking, Room


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def room_data():
    return {"description": "Luxury Suite", "price": 150.00}


@pytest.fixture
def booking_data(room):
    return {
        "room": room.id,
        "start_date": date.today() + timedelta(days=1),
        "end_date": date.today() + timedelta(days=3),
    }


@pytest.fixture
def room():
    return Room.objects.create(description="Standard Room", price=100.00)


@pytest.fixture
def booking(room):
    return Booking.objects.create(
        room=room,
        start_date=date.today() + timedelta(days=1),
        end_date=date.today() + timedelta(days=3),
    )
