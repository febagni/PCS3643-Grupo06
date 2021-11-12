from django.db import models
from django.urls import reverse
from django.conf import settings

# https://www.sothebysinstitute.com/news-and-events/news/auction-terminology

class Lot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    lot_name = models.CharField(max_length=200)
    reserve_price = models.IntegerField()
    sequential_uuid = models.CharField(max_length=200)
    minimal_bid = models.IntegerField()
    seller_contact = models.EmailField()
    lot_description = models.CharField(max_length=200)
    minimum_bid_increment = models.IntegerField()
    comissions = models.IntegerField()
    taxes = models.IntegerField()
    number_of_bids_made = models.IntegerField()
    current_winner_buyer = models.CharField(max_length=200)
    highest_value_bid = models.IntegerField()

    def get_lot_name(self):
        return self.lot_name

    def set_lot_name(self, new_lot_name):
        self.lot_name = new_lot_name
        return

    def get_reserve_price(self):
        return self.reserve_price

    def set_reserve_price(self, new_reserve_price):
        self.reserve_price = new_reserve_price
        return

    def get_absolute_url(self):
        return reverse('lot_user:lot_edit', kwargs={'pk': self.pk})