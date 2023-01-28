"""
User url configuration.
"""
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from . import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
    path("status/", views.CheckUserStatusView.as_view(), name="user-status"),
    path("logout/", views.UserLogoutView.as_view(), name="user-logout"),
    path("remove/", views.UserRemoveView.as_view(), name="user-remove"),
    path("deposit/", views.UserDepositView.as_view(), name="user-deposit"),
    path("reset/", views.UserResetView.as_view(), name="user-reset"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
