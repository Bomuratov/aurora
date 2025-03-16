from rest_framework import permissions
from rest_framework import response


perms_map = {
    'GET': ["can_view"],
    'POST': ['can_add'],
    'PUT': ['can_update'],
    'PATCH': ['can_update'],
    'DELETE': ['can_delete'],
}

class RoleCheck(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method not in perms_map:
            return response.Response({"error": "Такой метод не разрешен"}, status=405)
        required_perms = perms_map[request.method]
        print(user.role)
        if user.role is None and user.role.permissions is None:
            return False
        user_perms = user.role.permissions
        for perm in required_perms:
            role_based_perm = f"user_{user.role}_{perm}"
            if role_based_perm in user_perms:
                return True
        return False