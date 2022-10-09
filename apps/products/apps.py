"""
Products app configuration
"""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Products configuration
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
