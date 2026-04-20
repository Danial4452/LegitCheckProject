from rest_framework.permissions import BasePermission

# Только админ
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


# Владелец объекта или админ
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if request.user.is_staff:
            return True

        # для Product проверяем owner, для Comment — author
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return False
