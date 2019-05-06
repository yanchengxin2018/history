from rest_framework import serializers
from Main.models import *
from Main.tools import get_username,password_handler,get_num


from django.contrib.auth import get_user_model


#单词表
class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model=WordModel
        fields=('id','index','english','chinese','pronunciation',)
        # read_only_fields=('index','english','chinese','pronunciation',)


#单词零件
class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model=PartModel
        fields=('part','count',)


#用户表序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        fields=('id','mobile',)


#注册
class RegisterSerializer(serializers.Serializer):
    mobile=serializers.CharField(max_length=15)
    password=serializers.CharField()
    re_password=serializers.CharField()

    def validate_mobile(self, mobile):
        if not mobile:raise serializers.ValidationError('手机号不能为空')
        mobile=mobile.replace('+','')
        user_model=get_user_model()
        try:
            int(mobile)
            user_obj=user_model.objects.filter(mobile=mobile).first()
        except:
            raise serializers.ValidationError('手机号格式不合法')
        if user_obj:raise serializers.ValidationError('手机号已经存在')
        return mobile

    def validate(self,data):
        password=data.get('password')
        re_password=data.get('re_password')
        if password!=re_password:raise serializers.ValidationError({'error':'两次输入的密码不一致'})
        if not password:raise serializers.ValidationError({'error':'密码不能为空'})
        return data

    def create(self, validated_data):
        mobile=validated_data.get('mobile',None)
        password=validated_data.get('password',None)
        user_model=get_user_model()
        username=get_username()
        validate_sign=get_num(10)
        user_obj=user_model.objects.create(mobile=mobile,username=username,validate_sign=validate_sign)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


#登陆
class LoginSerializer(serializers.Serializer):
    mobile=serializers.CharField()
    password=serializers.CharField()

    def validate_mobile(self, mobile):
        user_model=get_user_model()
        user_obj=user_model.objects.filter(mobile=mobile).first()
        if not user_obj:raise serializers.ValidationError('手机号不存在')
        return user_obj

    def validate(self, data):
        user_obj=data.get('mobile')
        password=data.get('password')
        if not user_obj.check_password(password):
            raise serializers.ValidationError('用户名和密码不匹配')
        else:
            return data

    def create(self, validated_data):
        user_obj=validated_data.get('mobile')
        return user_obj


#记忆记录表
class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=RecordModel
        fields=('user_obj','word_obj','level',)












