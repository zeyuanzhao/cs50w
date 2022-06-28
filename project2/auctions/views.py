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
            new_watchlist = Watchlist(user=user)
            new_watchlist.save()
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

@login_required
def watchlist_add(request, id):
    if request.method == "POST":
        watchlist = request.user.watchlist.watchlist
        if watchlist.filter(id=id).exists():
            watchlist.remove(Listing.objects.get(id=id))
        else:
            watchlist.add(Listing.objects.get(id=id))
        return redirect("/listing/" + id)
    else:
        return redirect("/listing/" + id)

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
    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = request.user.watchlist.watchlist.filter(id=id).exists()
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(id=id),
        "commentform": CreateComment,
        "biderror": "",
        "bidform": CreateBid,
        "comments": Comment.objects.filter(listing=Listing.objects.get(id=id)),
        "watchlist": in_watchlist
    })

@login_required
def bid(request, id):
    if request.method == "POST":
        bid = CreateBid(request.POST)
        if not bid.is_valid():
            return redirect("/listing/" + id)
        bid = bid.save(commit=False)
        if Listing.objects.get(id=id).get_highest_bid > bid.amount:
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(id=id),
                "commentform": CreateComment,
                "biderror": "New bid must be greater than current bid",
                "bidform": CreateBid,
                "comments": Comment.objects.filter(listing=Listing.objects.get(id=id))
            })
        bid.user = request.user
        bid.listing = Listing.objects.get(id=id)
        bid.save()
        return redirect("/listing/" + id)
    else:
        return redirect("/listing/" + id)

@login_required
def comment(request, id):
    if request.method == "POST":
        comment = CreateComment(request.POST)
        if not comment.is_valid():
            return redirect("/listing/" + id)
        comment = comment.save(commit=False)
        comment.user = request.user
        comment.listing = Listing.objects.get(id=id)
        comment.save()
        return redirect("/listing/" + id)
    else:
        return redirect("/listing/" + id)