from rest_framework import permissions


class IsPublicationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (request.method in ('PATCH', 'PUT', 'DELETE') and
                not request.user.is_superuser and request.user != obj.creator):
            return False
        return True
