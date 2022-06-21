from ..models import *
from django.db.models import Max
from django import template

filter_register = template.Library()

@filter_register.filter
def get_highest_bid(listing):
    return listing.bid.filter(listing=listing.id).aggregate(Max('amount'))