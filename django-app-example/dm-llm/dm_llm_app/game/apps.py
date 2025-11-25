"""Django app configuration for game app."""

from django.apps import AppConfig


class GameConfig(AppConfig):
    """Django application configuration for the game app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "game"
