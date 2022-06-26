from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Max
from django import template
from django.forms import ModelForm, Textarea
from django.contrib.auth.decorators import login_required

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

class CreateListing(ModelForm):    
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]
        labels = {
            "starting_bid": "Starting Bid",
            "image_url": "Image URL"
        }
        widgets = {
            "description": Textarea(attrs={"rows": 3})
        }
    
    def __init__(self, *args, **kwargs):
        super(CreateListing, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control form-group", "placeholder": self.fields[field].label})
            self.fields[field].label = ""

@login_required
def create(request):
    if request.method == "POST":
        listing = CreateListing(request.POST)
        if not listing.is_valid():
            return render(request, "auctions/create.html", {
                "form": listing
        })
        listing = listing.save(commit=False)
        listing.user = request.user
        listing.save()
        return redirect("listing/" + str(listing.id))
    else:
        return render(request, "auctions/create.html", {
            "form": CreateListing
        })

@login_required
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

class CreateComment(ModelForm):
    class Meta():
        model = Comment
        fields = ["value"]
        labels = {
            "value": "Comment"
        }
        widgets = {
            "value": Textarea(attrs={"rows": 3})
        }
    def __init__(self, *args, **kwargs):
        super(CreateComment, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control form-group", "placeholder": self.fields[field].label})
            self.fields[field].label = ""

class CreateBid(ModelForm):
    class Meta():
        model = Bid
        fields = ["amount"]
    
    def __init__(self, *args, **kwargs):
        super(CreateBid, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control form-group", "placeholder": self.fields[field].label})
            self.fields[field].label = ""

def listing(request, id):
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(id=id),
        "commentform": CreateComment,
        "bidform": CreateBid,
        "comments": Comment.objects.filter(listing=Listing.objects.get(id=id))
    })

def bid(request, id):
    pass

def comment(request, id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(id=id),
                "form": CreateComment
            })
        comment = CreateComment(request.POST)
        if not comment.is_valid():
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(id=id),
                "form": CreateComment
            })
        comment = comment.save(commit=False)
        comment.user = request.user
        comment.listing = Listing.objects.get(id=id)
        comment.save()
        return redirect("/listing/" + id)