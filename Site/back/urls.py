from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from .views import *



back_router=DefaultRouter()
back_router.register(r'users',UsersViewSet)


urlpatterns = [
    # url('',)
]













