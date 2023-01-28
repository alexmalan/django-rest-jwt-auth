"""
Product url configuration.
"""
from django.urls import path

from . import views

urlpatterns = [
    path("list/", view=views.ProductListView.as_view(), name="product-list"),
    path("create/", view=views.ProductCreateView.as_view(), name="product-create"),
    path(
        "<int:product_id>/",
        view=views.ProductUpdateDeleteView.as_view(),
        name="product-update-delete",
    ),
    path(
        "<int:product_id>/buy/", view=views.ProductBuyView.as_view(), name="product-buy"
    ),
]
