from rest_framework.permissions import BasePermission


class SellerPermission(BasePermission):
    message = "You are not Seller"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_seller)
