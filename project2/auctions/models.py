from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from datetime import datetime

class User(AbstractUser):
    pass
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", null=True)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    starting_bid = models.IntegerField()
    image_url = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True)

    @property
    def get_highest_bid(self):
        return self.bids.filter(listing=self.id).aggregate(Max('amount'))["amount__max"]

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", null=True)
    amount = models.IntegerField(null=True)
    bid_time = models.DateTimeField(default=datetime.now, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    value = models.CharField(max_length=255, default="")

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist", null=True)
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchlist", null=True)
