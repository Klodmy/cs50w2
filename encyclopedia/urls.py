from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("wiki/<str:title>", views.titles, name="title"),
    path("search", views.search, name="search")
]

