from django.conf import settings
import datetime
from Questionnaire.models import Users as Questionnaire_Users
from rest_framework_jwt.settings import api_settings


#DRF的默认用户认证
class QuestionnaireAuthentication:

    def authenticate(self,request,*args,**kwargs):
        try:
            token=self.get_token(request)
            if not token:
                token =self.get_cookie_token(request)
            if not token:
                return(None,'JWT验证：token未携带或不正确')
            try:
                data=self.parse_token(token)
            except:
                return (None,token)
            if not self.valite_time(data):
                return(None,'JWT验证：token已过期')
            user=self.get_user(data)
            return (user,token)
        except:
            return (None,None)

    def get_user(self,data):
        username=data.get('username')
        user=Questionnaire_Users.objects.filter(username=username).first()
        # password=user.password
        # sys_user_model=get_user_model()
        # sys_user=sys_user_model.objects.filter(username=username).first()
        # if not sys_user:
        #     sys_user=sys_user_model.objects.create(username=username,password=password)
        return user

    def valite_time(self,data):
        #此刻
        now = datetime.datetime.now()
        #失效时间
        exp = data.get('exp')
        valite_range = datetime.datetime.utcfromtimestamp(exp)
        return valite_range > now

    def parse_token(self,token):

        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        data=jwt_decode_handler(token)
        return data

    def get_token(self,request):
        auth=request.META.get('HTTP_AUTHORIZATION', b'')
        if auth:
            sign = settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX']
            try:
                token=auth.split(sign+' ')[1]
                return token
            except:
                return None
        else:
            return None

    def get_cookie_token(self,request):
        auth=request.COOKIES.get('token',None)
        return auth if auth else None









