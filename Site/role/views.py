from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet as G,mixins as M
from Questionnaire.models import SchoolMaster as SchoolSchoolMasterModle
from role.serializers import SchoolSchoolHeadSerializer
from django.conf import settings
from django.db.models import Q


#创造一个校长
class CreateSchoolHeadViewSet(G):

    def list(self,request):

        create_user='{}/api/Questionnaire_Users/'.format(settings.ROOT_URL)
        bind_role='{}/api/Questionnaire_UsersRoles/'.format(settings.ROOT_URL)
        bind_school='{}/role/schoolschoolhead/'.format(settings.ROOT_URL)
        data={'create_user':create_user,'bind_role':bind_role,'bind_school':bind_school,}
        return render(request,'createschoolhead.html',data)


#创造一个用户并绑定到角色
class CreateUserRoleViewSet(G):

    def list(self,request):
        create_user='{}/api/Questionnaire_Users/'.format(settings.ROOT_URL)
        bind_role='{}/api/Questionnaire_UsersRoles/'.format(settings.ROOT_URL)
        data={'create_user':create_user,'bind_role':bind_role,}
        return render(request,'createuserrole.html',data)


#绑定用户和学校
class SchoolSchoolHeadViewSet(G,M.ListModelMixin,M.CreateModelMixin):
    queryset = SchoolSchoolMasterModle.objects.all().order_by('id')
    serializer_class =SchoolSchoolHeadSerializer

    def get_queryset(self):
        queryset=super().get_queryset()
        find=self.request.GET.get('查询',None)
        if find:
            queryset=queryset.filter(Q(user_obj__name__contains=find)|Q(user_obj__mobile__contains=find))
        return queryset.order_by('id')


