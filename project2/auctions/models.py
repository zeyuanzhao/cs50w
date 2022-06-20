from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models):
    pass

class Bid(models):
    pass

class Comment(models):
    pass