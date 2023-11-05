from rest_framework import permissions
from users.models import UserRoles


class IsOwner(permissions.BasePermission):
    message = 'Вы не являетесь владельцем данного объявления!'

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    message = 'Вы не администратор!'

    def has_permission(self, request, view):
        return request.user.role == UserRoles.ADMIN
