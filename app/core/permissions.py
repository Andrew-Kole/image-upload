from rest_framework import permissions


class IsPremiumUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Premium'


class IsEnterpriseUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Enterprise'


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'Admin'
