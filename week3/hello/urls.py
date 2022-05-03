from django.urls import path
from . import views

app_name = "hello"
urlpatterns = [
    path("", views.index, name="index"),
    path("world", views.world, name="world"),
    path("<str:name>", views.greet, name="greet")
]
