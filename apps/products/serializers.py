"""
Product serializer.
"""
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer.
    """

    class Meta:
        """
        Meta class.
        """

        model = Product
        fields = ("id", "name", "amount", "cost", "user")
        write_only_fields = (
            "name",
            "amount",
            "cost",
        )
        read_only_fields = (
            "id",
            "user",
        )
