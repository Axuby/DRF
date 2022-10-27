from rest_framework.permissions import DjangoModelPermissions, BasePermission, IsAdminUser, SAFE_METHODS


class IsAdminOrReadOnly(IsAdminUser):
    message = 'User '

    def has_permission(self, request, view):
        admin_perm = bool(request.user and request.user.is_staff)
        return admin_perm or request.method == "GET"
        # if request.method in SAFE_METHODS:
        #         return True
        #     else:
        # return super().has_permission(request, view)


class IsReviewUserOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.review_user == request.user or request.user.is_staff
        # return super().has_object_permission(request, view, obj)


class IsPermitted(DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view, obj):
        pass
