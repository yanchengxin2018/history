from django.utils.deprecation import MiddlewareMixin
from Main.authentication import Authentication
from django.http import HttpResponseRedirect


#只允许登陆用户
class IsAuthentication:
    """
    只允许登陆用户
    """
    message='权限限制:只允许登陆用户.'

    def has_permission(self, request, view):
        return bool(request.user)

    def has_object_permission(self, request, view, obj):
        return True


























