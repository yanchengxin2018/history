from rest_framework.viewsets import ModelViewSet
from .serializers import Users,UsersSerializer



#加载用户和角色
class UsersViewSet(ModelViewSet):
    queryset = Users.objects.get_queryset().order_by('id')
    serializer_class = UsersSerializer







