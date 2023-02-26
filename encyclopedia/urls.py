from django.urls import path
from . import util

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.titles, name="title"),
    path("search", views.search, name="search")
]

