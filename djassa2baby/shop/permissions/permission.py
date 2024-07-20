from rest_framework.permissions import BasePermission, SAFE_METHODS

class UnauthenticatedReadonly(BasePermission):
    """
    Custom permission to allow unauthenticated read-only access.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            # Autoriser les méthodes sûres (GET, HEAD, OPTIONS) sans authentification
            return True
        # Pour les autres méthodes (POST, PUT, DELETE, etc.), exiger l'authentification
        return request.user and request.user.is_authenticated

    
    from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role.label == 'client'

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'role') and request.user.role.label == 'vendeur'
