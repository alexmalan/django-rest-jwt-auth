"""
Users app configuration
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    User configuration
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
