from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to manage admin access.
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif view.action in ['create', 'destroy', 'invite', 'block']:
            return request.user.groups.filter(name='Admin').exists()
        elif view.action == 'manage_organization':
            return True
        return False


from rest_framework import permissions

class IsDeveloperPermission(permissions.BasePermission):
    """
    Custom permission to manage developer access.
    """
    SAFE_METHODS = ['list', 'retrieve']
    allowed_statuses = ['in_progress', 'done', 'review', 'approved', 'delivered', 'test']

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif view.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.groups.filter(name='Developer').exists()
        elif view.action == 'change_task_status':
            new_status = request.data.get('status', None)
            if new_status and new_status in self.allowed_statuses:
                return True
            return False
        elif view.action in self.SAFE_METHODS:
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        elif view.action == 'change_task_status':
            new_status = request.data.get('status', None)
            if new_status and new_status in self.allowed_statuses:
                return True
            return False
        elif view.action == 'destroy':
            return obj.assigned_to == request.user
        elif view.action in self.SAFE_METHODS:
            return True
        return False

    


    
