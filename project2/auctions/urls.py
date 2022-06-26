from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("listing/<str:id>/bid", views.bid, name="bid"),
    path("listing/<str:id>/comment", views.comment, name="comment")
]
