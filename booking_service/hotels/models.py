from django.db import models


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(
        "date of creation",
        auto_now_add=True,
        help_text="Date of creation",
    )
    updated_at = models.DateTimeField(
        "date of update",
        auto_now=True,
        help_text="Date of update",
    )

    class Meta:
        abstract = True


class Room(TimeStampMixin):
    objects = models.Manager()
    description = models.TextField("description", db_column="description")
    price = models.DecimalField(
        "price",
        decimal_places=2,
        max_digits=6,
        help_text="price per night at the room in dollars",
    )


class Booking(TimeStampMixin):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField("booking start date")
    end_date = models.DateField("booking end date")
