from django.db import models
from django.urls import reverse
from django.conf import settings

# https://www.sothebysinstitute.com/news-and-events/news/auction-terminology

class Auction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    auction_id = models.IntegerField()
    auction_start = models.IntegerField()
    auction_end = models.IntegerField()
    auctioneer = models.CharField(max_length=50)
    auction_winner = models.CharField(max_length=50)

    def set_auctioneer_info(self, name, id, contact):
        self.auctioneer_name = name
        self.auctioneer_id = id
        self.auctioneer_contact = contact
    
    def __str__(self):
        return self.auctioneer_name

    def get_absolute_url(self):
        return reverse('auctioneer:auction_edit', kwargs={'pk': self.pk})