from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Event, Customer, Contract

owner_methods = ('PUT', 'DELETE')


class hasCustomerPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in owner_methods:
            if obj.sales == request.user:
                return True

class hasContractPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in owner_methods:
            if obj.sales == request.user:
                return True


class hasEventPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in owner_methods:
            if obj.support == request.user or obj.contract.sales == request.user:
                return True