from rest_framework.request import Request
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class AbstractAuthentication:

    def authenticate(self,request,*args,**kwargs):
        self.request=request
        # self.kwargs=self.request._request.resolver_match.kwargs
        user=self.get_user()
        auth='这里不知道填什么东西[纠结]'
        return (user,auth)

    def get_user(self):
        user = SimpleLazyObject(lambda: self.get_user_jwt())
        return user

    def get_user_jwt(self):
        user = get_user(self.request)
        if user.is_authenticated:
            return user
        else:
            try:
                user_jwt = JSONWebTokenAuthentication().authenticate(Request(self.request))

                if user_jwt is not None:
                    return user_jwt[0]
            except:
                pass
            return None




