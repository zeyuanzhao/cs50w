from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<str:id>", views.watchlist_add, name="watchlistadd"),
    path("categories", views.categories, name="categories"),
    path("category/<str:c>", views.category, name="category"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("listing/<str:id>/bid", views.bid, name="bid"),
    path("listing/<str:id>/comment", views.comment, name="comment"),
    path("listing/<str:id>/end", views.listing_end, name="listingend"),
    path("closedlistings", views.closed_listings, name="closedlistings")
]
