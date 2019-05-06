from rest_framework import viewsets,permissions
from .models import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from Tools.tools import get_user_role

# 通过权限表查询权限
class PermissionTable(permissions.BasePermission):
    '''
    通过权限表查询权限
    '''
    message='没有访问权限或者资源不存在'

    #全局权限
    def has_permission(self, request, view):
        # return True
        if request.method =='OPTIONS':
            return True
        if '管理员' in get_user_role(request.user):
            return True
        resource='Questionnaire_'+view.__class__.__name__
        resource=self.get_resource(resource)
        if not resource:
            return False
        action=self.get_action(request)
        if ResourceRoleAction.objects.filter(resource=resource,action=action,role__role='所有人'):return True
        roles=self.get_roles(request)
        for role in roles:
            if ResourceRoleAction.objects.filter(resource=resource,action=action,role=role):
                return True

    #具体权限
    def has_object_permission(self, request, view, obj):
        if '管理员' in get_user_role(request.user): return True
        resource = view.__class__.__name__
        resource = self.get_resource(resource)
        if not resource:
            return False
        action = self.get_action(request,pk=True)
        if ResourceRoleAction.objects.filter(resource=resource, action=action, role='所有人'): return True
        roles = self.get_roles(request)
        for role in roles:
            if ResourceRoleAction.objects.filter(resource=resource, action=action, role=role):
                return True

    #得到注册的资源对象
    def get_resource(self,resource):
        resource=resource.replace('ViewSet','')
        resource=Resources.objects.filter(resource=resource)

        if resource:
            return resource.first()
        else:
            return None

    #得到访问动作
    def get_action(self,request,pk=False):
        user_method=request.method
        #访问集合1/增加集合2/修改具体3/删除具体4/访问具体5/
        action_info={
            # 1:('GET', 'HEAD', 'OPTIONS'),
            1: ('GET', 'HEAD',),
            3: ('POST',),
            4: ('PUT','PATCH',),
            5: ('DELETE',),
            6: ('OPTIONS',),
        }
        key=None
        for model in action_info:
            if user_method in action_info[model]:
                key=model
                break
        #如果当前请求是操作具体(pk=True)发起,并且为访问模式,那当前动作就为[访问具体5]
        if key==1 and pk:
            key=2
        action=Action.objects.filter(action=key).first()
        if not action:
            info='缺省的帮助信息：模式{}的请求方式为{}'.format(key,action_info[key]) if key!=5 else '缺省的帮助信息：访问具体'
            action=Action(action=key,help=info)
            action.save()
        return action

    #得到角色/可能是多个,统一使用数组格式返回
    def get_roles(self,request):
        '匿名用户被添加到匿名用户角色,不存在将创建'
        user=request.user
        if not user:
            role='匿名用户'
            role_obj=Roles.objects.filter(role=role)
            if role_obj:
                return role_obj
            else:
                # Roles.objects.create(role=role)
                role=Roles(role=role)
                role.save()
                return self.get_roles(request)
        else:
            usersroles_objs=UsersRoles.objects.filter(user=user)
            roles=[]
            for usersroles_obj in usersroles_objs:
                roles.append(usersroles_obj.role)
            return roles


# 没有验证的老师没有任何权限
class IsValidateTeacher(permissions.BasePermission):
    '''
    没有验证的老师没有任何权限
    '''
    message='还没有通过验证的老师'

    #全局权限
    def has_permission(self, request, view):
        user=request.user
        if '老师' in get_user_role(user):
            teacher_obj=Teacher.objects.filter(user=user).first()
            if not teacher_obj:
                return False
            if teacher_obj.is_valied:
                return True
            else:
                return False
        else:
            return True













