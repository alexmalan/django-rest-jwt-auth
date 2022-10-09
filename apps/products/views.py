"""
Product views.
"""
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from common.permissions import IsBuyer, IsOwner, IsSeller

from .models import Product
from .serializers import ProductSerializer
from .services import buy_product


class ProductListView(generics.ListAPIView):
    """
    List all products.

    * Requires session authentication.
    """

    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductCreateView(generics.CreateAPIView):
    """
    Create products.

    * Requires session authentication.
    """

    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]

    def perform_create(self, serializer):
        """
        Perform create product.
        """
        serializer.save(user=self.request.user)


class ProductUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Update and Delete products.

    * Requires session authentication.
    """

    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller, IsOwner]

    def get_object(self):
        """
        Retrieve product.

        ```
        :raise: ValidationError if product not found or is invalid
        ```
        """
        try:
            product = Product.objects.get(id=self.kwargs.get("product_id"))
        except:
            raise ValidationError("Product not found")
        return product

    def update(self, request, *args, **kwargs):
        """
        Update product.

        ```
        :param Request request: client request with authorization in header
        :return: Empty response with status 200
        ```
        """
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete product.

        ```
        :return: Response with status 204
        ```
        """
        product = self.get_object()
        product.delete()
        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProductBuyView(generics.GenericAPIView):
    """
    Buy products.

    * Requires session authentication.
    """

    queryset = Product.objects.all()
    model = Product
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]

    def post(self, request, *args, **kwargs):
        """
        Buy product.

        ```
        :param Request request: client request with authorization in header
        :return: Empty response with status 200
        :raise: ValidationError if product not found or is invalid
        ```
        """
        if not request.data:
            raise ValidationError("Invalid payload")

        if self.kwargs["product_id"]:
            request.data["product_id"] = self.kwargs["product_id"]
        else:
            raise ValidationError("No product provided")

        change_list, spending, product = buy_product(request.user, request.data)

        if product:
            report = {
                "change": change_list,
                "spending": spending,
                "product": ProductSerializer(product).data,
            }

            return Response({"response": report}, status=status.HTTP_200_OK)
        raise ValidationError("Product not found")
