from rest_framework import serializers
from Questionnaire.models import SchoolMaster as SchoolSchoolMasterModle,UsersRoles as UsersRolesModel
from django.conf import settings



class SchoolSchoolHeadSerializer(serializers.ModelSerializer):
    school_name=serializers.CharField(source='school_obj.school_name',read_only=True)
    user_name=serializers.CharField(source='user_obj.name',read_only=True)
    user_mobile=serializers.CharField(source='user_obj.mobile',read_only=True)
    class Meta:
        model=SchoolSchoolMasterModle
        fields=('user_obj','school_obj','school_name','user_name','user_mobile',)

    def validate_user_obj(self, user_id):
        #验证角色是不是校长
        SCHOOLHEAD=settings.SCHOOLHEAD
        if not UsersRolesModel.objects.filter(user_obj__id=user_id,role__role=SCHOOLHEAD):
            raise serializers.ValidationError({'error':'不可以绑定到一个非校长角色'})
        else:
            return user_id

























