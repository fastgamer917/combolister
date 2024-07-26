from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload", views.upload_combos, name="upload_combo"),
    path("search", views.search, name="search"),
    path("searchv2", views.searchv2, name="search V2"),
]