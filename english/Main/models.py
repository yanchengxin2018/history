from django.db import models
from django.contrib.auth.models import AbstractUser


#用户表
class UserModel(AbstractUser):
    mobile=models.CharField(max_length=15,unique=True)
    validate_sign=models.CharField(max_length=20)
    def __str__(self):
        return self.mobile

#单词表
class WordModel(models.Model):
    index=models.IntegerField()
    english=models.CharField(max_length=100)
    chinese=models.CharField(max_length=100)
    pronunciation=models.CharField(max_length=100)


#单词零件
class PartModel(models.Model):
    part=models.CharField(max_length=100)
    count=models.IntegerField(default=1)


#记录表
class RecordModel(models.Model):
    user_obj=models.ForeignKey(to='UserModel',on_delete=models.CASCADE)
    word_obj=models.ForeignKey(to='WordModel',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    level=models.IntegerField(default=0)


#熟词表
class FamiliarModel(models.Model):
    user_obj=models.ForeignKey(to='UserModel',on_delete=models.CASCADE)
    word_obj=models.ForeignKey(to='WordModel',on_delete=models.CASCADE)



























