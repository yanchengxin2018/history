
from rest_framework.routers import DefaultRouter
from role import views


role_router=DefaultRouter()
role_router.register(r'schoolschoolhead',views.SchoolSchoolHeadViewSet)
role_router.register(r'CreateSchoolHead',views.CreateSchoolHeadViewSet,base_name='CreateSchoolHead')
role_router.register(r'CreateUserRole',views.CreateUserRoleViewSet,base_name='CreateUserRole')










