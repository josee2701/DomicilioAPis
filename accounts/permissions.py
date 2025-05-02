
from rest_framework import permissions


class IsAdmin (permissions.BasePermission):
    """Permiso si el usuario es un administrador."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()

class IsClient (permissions.BasePermission):
    """Permiso si el usuario es un cliente."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Client').exists()
    
class IsDriver (permissions.BasePermission):
    """Permiso si el usuario es un conductor."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Driver').exists()