"""
Common project permissions.
"""
from rest_framework import permissions


class IsSeller(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object perform actions on it.
    """

    def has_permission(self, request, view):
        return request.user.role == "SELLER"


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object perform actions on it.
    """

    def has_permission(self, request, view):
        return request.user.id == view.get_object().user.id


class IsBuyer(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object perform actions on it.
    """

    def has_permission(self, request, view):
        return request.user.role == "BUYER"
