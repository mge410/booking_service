from django.db import models
from django.utils import timezone


class Room(models.Model):
    objects = models.Manager()
    description = models.TextField("description", db_column="description")
    price = models.DecimalField(
        "price",
        decimal_places=2,
        max_digits=6,
        help_text="price per night at the room in dollars",
    )
    created_at = models.DateTimeField(
        "date of creation",
        default=timezone.now,
        help_text="Date of creation",
    )


class Booking(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField("booking start date")
    end_date = models.DateField("booking end date")
