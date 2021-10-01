from django.db import models
from django.urls import reverse

# https://www.sothebysinstitute.com/news-and-events/news/auction-terminology

class Lot(models.Model):
    lot_name = models.CharField(max_length=200)
    reserve_price = models.IntegerField()
    sequential_uuid = models.IntegerField()
    minimal_bid = models.IntegerField()
    lot_photo = models.CharField(max_length=200)
    seller_contact = models.IntegerField()
    lot_description = models.CharField(max_length=200)
    minimum_bid_increment = models.IntegerField()
    comissions = models.IntegerField()
    taxes = models.IntegerField()
    number_of_bids_made = models.IntegerField()
    current_winner_buyer = models.CharField(max_length=200)
    highest_value_bid = models.IntegerField()

    def __str__(self):
        return self.lot_name

    def get_absolute_url(self):
        return reverse('lot:lot_edit', kwargs={'pk': self.pk})