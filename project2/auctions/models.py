from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from datetime import datetime

class Listing(models.Model):
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    starting_bid = models.IntegerField()
    image_url = models.CharField(max_length=512)
    category = models.CharField(max_length=32)

    @property
    def get_highest_bid(self):
        return self.bid.filter(listing=self.id).aggregate(Max('amount'))["amount__max"]

class User(AbstractUser):
    watchlist  = models.ManyToManyField(Listing, blank=True, related_name="watchlist")

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid", null=True)
    amount = models.IntegerField(null=True)
    bid_time = models.DateTimeField(default=datetime.now, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    value = models.CharField(max_length=512, default="")