from django.db import models
from django.urls import reverse

# https://www.sothebysinstitute.com/news-and-events/news/auction-terminology

class Auction(models.Model):
    auction_id = models.IntegerField()
    auction_start = models.IntegerField()
    auction_end = models.IntegerField()
    auctioneer = models.CharField(max_length=50)
    auction_status = models.CharField(max_length=50)
    auction_published = models.BooleanField()

    def __str__(self):
        return self.auction_id

    def get_absolute_url(self):
        return reverse('auction:auction_edit', kwargs={'pk': self.pk})

