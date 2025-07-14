from django.db import models


class Hotel(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField("description")
    price = models.DecimalField(
        "price",
        decimal_places=2,
        max_digits=6,
        help_text="price per night at the hotel in dollars",
    )


class Booking(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField("booking start date")
    end_date = models.DateField("booking end date")
