from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload", views.upload_combos, name="upload_combo"),
    path("search", views.search, name="search"),
    path("searchv2", views.searchv2, name="search V2"),
    path("submit_search", views.submit_search, name="submit_search"),
    path("search_progress", views.search_progress, name="search_progress"),
    path("search_results", views.search_results, name="search_results"),
    path("delete_search_results", views.delete_search_results, name="delete_search_results"),
]