"""URL configuration for game app."""

from django.urls import path

from .views import dungeon_view

urlpatterns = [
    path("dungeon/", dungeon_view, name="dungeon"),
]
