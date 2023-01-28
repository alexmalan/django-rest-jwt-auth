"""
User views.
"""
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from common.permissions import IsBuyer

from .models import User
from .serializers import RegisterSerializer
from .services import deposit_amount, reset_amount


# REGISTER
class UserRegisterView(generics.CreateAPIView):
    """
    User registration.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer


# STATUS
class CheckUserStatusView(generics.RetrieveAPIView):
    """
    Check user status.

    * Requires Authentication header with token.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve user status.

        ```
        :param Request request: client request with authorization in header
        :return: Response with status 200
        ```
        """
        return Response(
            {"success": f"Logged in as: {request.user} : {request.user.role}"},
            status=status.HTTP_200_OK,
        )


# LOGOUT
class UserLogoutView(generics.RetrieveAPIView):
    """
    Logout user.

    * Requires Authentication header with token.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Logout user.

        ```
        :param Request request: client request with authorization in header
        :return: Response with status 200
        ```
        """
        try:
            token = RefreshToken(request.data.get("refresh"))
            token.blacklist()

            return Response(
                {"success": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST
            )


# REMOVE
class UserRemoveView(generics.RetrieveUpdateDestroyAPIView):
    """
    Remove user.

    * Requires Authentication header with token.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(
            {"success": "User Removed Successfully"}, status=status.HTTP_200_OK
        )


class UserDepositView(generics.GenericAPIView):
    """
    Deposit amount in user account.

    * Requires Authentication header with token.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]

    def post(self, request):
        """
        User deposit.

        ```
        :param Request request: client request with authorization in header
        :return: Response with status 200
        :raise: Validation error with status 400
        ```
        """
        if request.data is None or not request.data["amount"]:
            raise ValidationError("Invalid input")

        response = deposit_amount(request.user, request.data["amount"])

        if response:
            return Response(
                {
                    "success": f"Deposit successful. Your new balance is {request.user.deposit}"
                },
                status=status.HTTP_200_OK,
            )


class UserResetView(generics.GenericAPIView):
    """
    Reset user deposit amount.

    * Requires Authentication header with token.
    """

    queryset = User.objects.all()
    model = User
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsBuyer]

    def post(self, request):
        """
        Reset user deposit.

        ```
        :param Request request: client request with authorization in header
        :return: Response with status 200
        :raise: Validation error with status 400
        ```
        """
        response = reset_amount(request.user)

        if response:
            return Response(
                {
                    "success": f"Deposit reset successful. Your available balance is {request.user.deposit}"
                },
                status=status.HTTP_200_OK,
            )
        raise ValidationError("Something went wrong")
