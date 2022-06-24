from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django import template
from django.forms import ModelForm

from .models import *
# from .helper import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class CreateForm(ModelForm):    
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]
    
    def __init__(self, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control form-group", "placeholder": self.fields[field].label})
            self.fields[field].label = ""

def create(request):
    if request.method == "POST":
        listing = request.POST
    else:
        return render(request, "auctions/create.html", {
            "form": CreateForm
        })

def watchlist(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "auctions/watchlist.html")

def categories(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "auctions/categories.html")

def listing(request, name):
    if request.method == "POST":
        pass
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing
        })