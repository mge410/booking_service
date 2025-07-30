import pytest
from django.urls import reverse
from rest_framework import status
from hotels.models import Room, Booking
from datetime import date, timedelta


@pytest.mark.django_db
class TestRoomEndpoints:
    def test_create_room(self, client, room_data):
        url = reverse("room-list")
        response = client.post(url, room_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert Room.objects.count() == 1

    def test_list_rooms(self, client, room):
        url = reverse("room-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == room.id
        assert response.data[0]["description"] == room.description
        assert float(response.data[0]["price"]) == float(room.price)

    def test_list_rooms_ordering(self, client):
        Room.objects.create(description="Room 1", price=100.00)
        Room.objects.create(description="Room 2", price=150.00)

        url = reverse("room-list")
        response = client.get(url, {"ordering": "price"})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert float(response.data[0]["price"]) == 100.00
        assert float(response.data[1]["price"]) == 150.00

        response = client.get(url, {"ordering": "-price"})
        assert float(response.data[0]["price"]) == 150.00
        assert float(response.data[1]["price"]) == 100.00

    def test_delete_room(self, client, room):
        url = reverse("room-detail", kwargs={"pk": room.id})
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Room.objects.count() == 0


@pytest.mark.django_db
class TestBookingEndpoints:
    def test_create_booking(self, client, room, booking_data):
        url = reverse("booking-list")
        response = client.post(url, booking_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert Booking.objects.count() == 1

    def test_create_booking_invalid_dates(self, client, room):
        url = reverse("booking-list")
        data = {
            "room": room.id,
            "start_date": date.today() + timedelta(days=3),
            "end_date": date.today() + timedelta(days=1),
        }
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "End date must be after start date" in str(response.data)

    def test_list_bookings_without_room_param(self, client, booking):
        url = reverse("booking-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Room parameter room is required" in str(response.data)

    def test_list_bookings_with_room_param(self, client, room, booking):
        url = reverse("booking-list")
        response = client.get(url, {"room": room.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == booking.id
        assert response.data[0]["room"] == room.id

    def test_list_bookings_with_invalid_room_id(self, client):
        url = reverse("booking-list")
        response = client.get(url, {"room": "invalid"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Room ID must be a valid integer" in str(response.data)

    def test_list_bookings_ordering(self, client, room):
        booking1 = Booking.objects.create(
            room=room,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=3),
        )
        booking2 = Booking.objects.create(
            room=room,
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=7),
        )

        url = reverse("booking-list")
        response = client.get(url, {"room": room.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]["id"] == booking1.id
        assert response.data[1]["id"] == booking2.id

    def test_delete_booking(self, client, booking):
        url = reverse("booking-detail", kwargs={"pk": booking.id})
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Booking.objects.count() == 0
