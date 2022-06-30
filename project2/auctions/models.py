from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max
from datetime import datetime

class User(AbstractUser):
    pass
class Listing(models.Model):
    CATEGORIES = (
        ("Electronics", "Electronics"),
        ("Furniture", "Furniture"),
        ("Real Estate", "Real Estate"),
        ("Tools", "Tools"),
        ("Clothes", "Clothes"),
        ("Toys", "Toys"),
        ("Office", "Office"),
        ("Art", "Art"),
        ("Instruments", "Instruments"),
        ("Software", "Software"),
        ("Antiques", "Antiques")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", null=True, blank=True)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    title = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=255, blank=False)
    starting_bid = models.IntegerField(blank=False)
    image_url = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True, choices=CATEGORIES)
    ended = models.BooleanField(default=False, null=False, blank=True)

    @property
    def get_highest_bid(self):
        bid = self.bids.filter(listing=self.id).aggregate(Max('amount'))["amount__max"]
        return bid if bid else self.starting_bid

    @property
    def get_highest_bidder(self):
        return self.bids.get(amount=self.get_highest_bid).user

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", null=True, blank=True)
    amount = models.IntegerField(null=True, blank=False)
    bid_time = models.DateTimeField(default=datetime.now, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    value = models.CharField(max_length=255, default="", blank=False)

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist", null=True, blank=True)
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchlist", null=True)
