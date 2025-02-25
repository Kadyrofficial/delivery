from rest_framework.permissions import BasePermission
from .models import User


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(request.user and request.user.type == User.UserType.SUPERUSER)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(request.user and request.user.type == User.UserType.ADMIN)


class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(request.user and request.user.type in [User.UserType.ADMIN, User.UserType.SUPERUSER])


class IsClient(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(request.user and request.user.type == User.UserType.CLIENT)


class IsDelivery(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(request.user and request.user.type == User.UserType.DELIVERY)


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return bool(request.user and request.user.type == User.UserType.CUSTOMER)
