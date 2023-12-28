from rest_framework import permissions


class IsManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # On évite l'erreur où un utilisateur n'est pas authentifié et est "anonymous", il ne possède pas de groupe
        if request.user.is_authenticated:
            return request.user.group.name == "Gestion"
        return False


class IsSalesPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # On évite l'erreur où un utilisateur n'est pas authentifié et est "anonymous", il ne possède pas de groupe
        if request.user.is_authenticated:
            return request.user.group.name == "Vente"


class IsSupportPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # On évite l'erreur où un utilisateur n'est pas authentifié et est "anonymous", il ne possède pas de groupe
        if request.user.is_authenticated:
            return request.user.group.name == "Support"
