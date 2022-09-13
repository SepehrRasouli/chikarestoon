from rest_framework.permissions import BasePermission,SAFE_METHODS
class IsUserChangingTheirOwnProfile(BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and
            request.user == obj.user or
            request.user.is_staff
        )

class IsTheUserDoingActionsOnTheirOwnProfile(BasePermission):
    def has_permission(self,request,view):
        is_user_changing_his_own_post = True
        if request.method == 'POST' and request.data != {}:
            is_user_changing_his_own_post = request.user.pk == int(request.data['author'])
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated and
            is_user_changing_his_own_post
        )


