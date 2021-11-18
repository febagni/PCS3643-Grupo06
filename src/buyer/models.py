from django.db import models
from django import forms
from django.urls import reverse
from django.conf import settings

# https://www.sothebysinstitute.com/news-and-events/news/auction-terminology

class Buyer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    auction_id = models.IntegerField()
    lot_id = models.IntegerField()
    bid_value = models.IntegerField()
    
    def __str__(self):
        return str(self.bid_value)

    def get_absolute_url(self):
        return reverse('auction:make_bid', kwargs={'pk': self.pk})
