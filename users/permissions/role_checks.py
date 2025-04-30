from rest_framework import permissions
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


perms_map = {
    'GET': "can_view",
    'POST': "can_add",
    'PUT': "can_update",
    'PATCH': "can_update",
    'DELETE': "can_delete",
}

class RoleCheck(permissions.BasePermission):
        
    
    def has_permission(self, request, view):
        user = request.user
        model_name = view.queryset.model.__name__.lower()

        logger.info(user.get_user_role_perms())
        logger.info(model_name)
        

        if request.method not in perms_map:
            return False
        
        required_perms = perms_map[request.method]
        logger.info(required_perms)

        if user.get_user_role() is None and user.get_user_role_perms() is None:
            return False
        
        user_perms = user.get_user_role_perms()
        logger.info(user_perms)

        req_perms = f"{required_perms}_{model_name}"
        logger.info(req_perms)

        if req_perms in user_perms:
            return True
        
        return False
    

class PermissionCheck(permissions.BasePermission):
        
    def has_permission(self, request, view):
        user = request.user
        model_name = view.queryset.model.__name__.lower()

        if request.method not in perms_map:
            return False
        
        required_perms = perms_map[request.method]

        if user.get_custom_permissions() is None:
            return False
        
        user_perms = user.get_custom_permissions()

        req_perms = f"{required_perms}_{model_name}"

        if req_perms in user_perms:
            return True
        
        return False