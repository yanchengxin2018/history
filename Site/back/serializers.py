from rest_framework import serializers
from Questionnaire.models import Users,UsersRoles


#用户
class UsersSerializer:
    role=serializers.SerializerMethodField()

    def get_role(self,obj):
        return ''

    class Meta:
        model=Users
        fields=('id','name','mobile','role',)





