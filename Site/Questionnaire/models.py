from django.db import models
from django.contrib.auth.models import AbstractUser
#Prov
# questionnaire_type Task User
# ---------------------------------------------------------------------------- A


#动作表
class Action(models.Model):
    '''
    访问动作
    '''
    action=models.IntegerField(help_text='此动作用一个数字表示')
    help=models.TextField(help_text='动作的描述')
    def __str__(self):
        return self.help


# ---------------------------------------------------------------------------- B
# ---------------------------------------------------------------------------- C

#临时沟通表
class chat(models.Model):
    name=models.CharField(max_length=100,default='匿名')
    created_at=models.DateTimeField(auto_now=True)
    centext=models.CharField(max_length=100)

#手机验证码
class Codes(models.Model):
    code=models.CharField(max_length=10)
    created_at=models.DateTimeField(auto_now=True)
    mobile=models.CharField(max_length=15)
    type=models.IntegerField(choices=((1,'注册'),(2,'改密')),help_text='1为注册,2为修改密码')


#学生班级
class ClassStudent(models.Model):
    s_class=models.ForeignKey(to='Class',on_delete=models.CASCADE)
    student=models.ForeignKey(to='Student',on_delete=models.CASCADE)
    class Meta:
        unique_together=('s_class','student',)


#班级
class Class(models.Model):
    class_name=models.CharField(max_length=15,help_text='班级名称')
    def __str__(self):
        school_obj = School.objects.filter(schoolgrade__grade__gradeclass__class_name=self).first()
        grade_obj = Grade.objects.filter(gradeclass__class_name=self).first()
        args = (school_obj.school_name, grade_obj.grade_name, self.class_name)
        info = '学校[{}]年级[{}]班级[{}]'.format(*args)
        return info


#绑定老师与班级
class ClassTeacher(models.Model):
    teacher=models.ForeignKey(to='Teacher',on_delete=models.CASCADE,help_text='选择老师')
    class_name=models.ForeignKey(to='Class',on_delete=models.CASCADE,help_text='选择班级')


#班级问卷绑定
class ClassQuestionnaire(models.Model):
    class_obj=models.ForeignKey(to='Class',on_delete=models.CASCADE)
    questionnaire_obj=models.ForeignKey(to='Questionnaire',on_delete=models.CASCADE)
    def __str__(self):
        info='班级{}：问卷{}'.format(self.class_obj.class_name,
                                self.questionnaire_obj.questionnaire_name)
        return info
    class Meta:
        unique_together=('class_obj','questionnaire_obj',)


#城市
class City(models.Model):
    create_at=models.DateTimeField(auto_now=True)
    city_name=models.CharField(max_length=50)
    province_obj=models.ForeignKey(to='Province',on_delete=models.CASCADE)
    def __str__(self):
        return '{}{}'.format(self.province_obj.province_name,self.city_name)

#城市学校关联表
class CitySchool(models.Model):
    city_obj=models.ForeignKey(to='City',on_delete=models.CASCADE)
    school_obj=models.ForeignKey(to='School',on_delete=models.CASCADE)
    class Meta:
        unique_together=('city_obj','school_obj',)

#城市添加城市负责人
class CityCityHead(models.Model):
    city_obj=models.ForeignKey(to='City',on_delete=models.CASCADE)
    city_head_obj=models.ForeignKey(to='Users',on_delete=models.CASCADE)
    class Meta:
        unique_together=('city_obj','city_head_obj',)


# ---------------------------------------------------------------------------- D
# ---------------------------------------------------------------------------- E


#问卷被错误提交
class ErrorCommit(models.Model):
    #原始数据：名字.学校.年级.班级.问卷编号 /提交失败的类型/提交失败的详细说明/
    create_at=models.DateTimeField(auto_now=True)
    original_name=models.CharField(max_length=100)
    original_school=models.CharField(max_length=100)
    original_grade=models.CharField(max_length=100)
    original_class=models.CharField(max_length=100)
    original_code=models.CharField(max_length=100)
    choices=(
        (1,'问卷里提供的信息不足以查询到这个学生'),
        (2,'提交者信息被匹配为学校的学生但是未被邀请填写问卷'),
        (3,'所属任务因为[已提交/已过期等原因]已经关闭'),
        (4,'匹配到多个学生,并且多个学生都拥有这份问卷,系统不知道具体是哪一个问卷任务'),
        (5,'此问卷没有在服务器注册,请及时注册,以免耽误正常业务.'),
        (6,'通过提交的信息匹配到多个学生,但是所有的学生都没有被邀请.'),
    )
    error_type=models.CharField(max_length=100,choices=choices)
    error_help=models.TextField()


# ---------------------------------------------------------------------------- F
# ---------------------------------------------------------------------------- G


#年级
class Grade(models.Model):
    grade_name=models.CharField(max_length=50,help_text='输入年级名称')
    def __str__(self):
        school=School.objects.filter(schoolgrade__grade=self).first()
        if school:
            return '{}|{}'.format(school.school_name,self.grade_name)
        else:
            return '{}|{}'.format('没有找到对应的学校',self.grade_name)


#班级年级
class GradeClass(models.Model):
    class_name=models.ForeignKey(to='Class',on_delete=models.CASCADE)
    grade=models.ForeignKey(to='Grade',on_delete=models.CASCADE)
    class Meta:
        unique_together=('class_name','grade',)


#年级添加年级主任
class GradeGradeHead(models.Model):
    grade_obj=models.ForeignKey(to='Grade',on_delete=models.CASCADE)
    grade_head_obj=models.ForeignKey(to='Users',on_delete=models.CASCADE)






# ---------------------------------------------------------------------------- H
# ---------------------------------------------------------------------------- I
# ---------------------------------------------------------------------------- J
# ---------------------------------------------------------------------------- K
# ---------------------------------------------------------------------------- L
# ---------------------------------------------------------------------------- M


#问卷虽然被错误提交,但成功匹配到了一个或者多个任务/学生,这个表记录这些匹配并与ErrorCommit关联
class MatchButError(models.Model):
    matchstudent_obj=models.ForeignKey(to='Student',on_delete=models.CASCADE,null=True)
    matchstudentquestionnaire_obj=\
        models.ForeignKey(to='StudentQuestionnaire',on_delete=models.CASCADE,null=True)
    matcherrorcommit_obj=\
        models.ForeignKey(to='ErrorCommit',on_delete=models.CASCADE)


# ---------------------------------------------------------------------------- N
# ---------------------------------------------------------------------------- O
# ---------------------------------------------------------------------------- P


#省
class Province(models.Model):
    create_at=models.DateTimeField(auto_now=True)
    province_name=models.CharField(max_length=50)
    def __str__(self):
        return self.province_name


#省添加省负责人
class ProvinceProvinceHead(models.Model):
    province_obj=models.ForeignKey(to='Province',on_delete=models.CASCADE)
    province_head_obj=models.ForeignKey(to='Users',on_delete=models.CASCADE)
    class Meta:
        unique_together=('province_obj','province_head_obj',)


# ---------------------------------------------------------------------------- Q


# 问卷
class Questionnaire(models.Model):
    create_at=models.DateField(auto_now=True)
    created_at=models.DateTimeField(auto_now=True)
    questionnaire_url=models.CharField(max_length=100,help_text='问卷的链接',unique=True)
    questionnaire_code = models.CharField(max_length=100, help_text='问卷的唯一编码',unique=True)
    questionnaire_name=models.CharField(max_length=100,help_text='问卷的名字')
    questionnaire_type=models.ForeignKey(to='QuestionnaireType',on_delete=False,help_text='问卷的类型')
    # school_name_field = \
    #     models.IntegerField(help_text='告诉服务器问卷里学生的学校填在了哪个字段[例如field_13就填13即可]')
    grade_name_field= \
        models.IntegerField(help_text='告诉服务器问卷里学生的年级填在了哪个字段[例如field_14就填14即可]')
    class_name_field = \
        models.IntegerField(help_text='告诉服务器问卷里学生的班级填在了哪个字段[例如field_15就填15即可]')
    student_name_field=\
        models.IntegerField(help_text='告诉服务器问卷里学生的姓名填在了哪个字段[例如field_16就填16即可]')
    sms_status=models.BooleanField(default=False)
    def __str__(self):
        return '{}[唯一编号:{}]'.format(self.questionnaire_name,self.questionnaire_code)


# 问卷类型
class QuestionnaireType(models.Model):
    type_name=models.CharField(max_length=50,help_text='添加问卷类型[例如学生问卷家长问卷]',unique=True)
    help=models.TextField(help_text='备注信息',null=True)
    def __str__(self):
        return self.type_name


# ---------------------------------------------------------------------------- R


#权限表
class ResourceRoleAction(models.Model):
    '''
    资源-角色-动作  3个信息判断是否有权限
    '''
    create_at=models.DateTimeField(auto_now=True)
    update_at=models.DateTimeField(auto_now_add=True)
    resource=models.ForeignKey(to='Resources',on_delete=models.CASCADE,help_text='在此处选择接口')
    role=models.ForeignKey(to='Roles',on_delete=models.CASCADE,help_text='选择角色')
    action=models.ForeignKey(to='Action',on_delete=models.CASCADE,help_text='选择动作')
    class Meta:
        unique_together=('role','action','resource')

#角色表
class Roles(models.Model):
    '''
    角色表
    '''
    role=models.CharField(max_length=10,help_text='为角色命名',unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.role


#资源表
class Resources(models.Model):
    '''
    资源表/接口
    '''
    resource=models.CharField(max_length=50,help_text='接口的完整类名在此注册')
    help=models.TextField(help_text='输入接口的帮助信息',null=True)
    def __str__(self):
        return self.help


# ---------------------------------------------------------------------------- S


#学生
class Student(models.Model):
    user=models.OneToOneField(to='Users',on_delete=models.CASCADE,help_text='绑定用户')
    def __str__(self):
        return self.user.username


#学生问卷绑定
class StudentQuestionnaire(models.Model):
    create_at=models.DateField(auto_now=True)
    student_obj=models.ForeignKey(to='Student',on_delete=models.CASCADE)
    questionnaire_obj=models.ForeignKey(to='Questionnaire',on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    class Meta:
        unique_together=('student_obj','questionnaire_obj',)
    def __str__(self):
        info='学生：{}|问卷：{}'.format(self.student_obj.user.username,
                                  self.questionnaire_obj.questionnaire_name)
        return info


#学校
class School(models.Model):
    school_name=models.CharField(max_length=100,help_text='输入学校的名称')
    def __str__(self):
        return self.school_name


#校长
class SchoolMaster(models.Model):
    user_obj=models.ForeignKey(to='Users',on_delete=models.CASCADE)
    school_obj=models.ForeignKey(to='School',on_delete=models.CASCADE)
    def __str__(self):
        return '学校：{}|校长：{}'.format(self.school_obj.school_name,self.user_obj.username)


#学校年级
class SchoolGrade(models.Model):
    school=models.ForeignKey(to='School',on_delete=models.CASCADE)
    grade=models.ForeignKey(to='Grade',on_delete=models.CASCADE)
    class Meta:
        unique_together=('school','grade',)


# ---------------------------------------------------------------------------- T


#老师的问卷
class TeacherQuestionnaire(models.Model):
    teacher=models.ForeignKey(to='Teacher',on_delete=models.CASCADE,help_text='绑定老师')
    questionnaire=models.ForeignKey(to='Questionnaire',on_delete=models.CASCADE,help_text='绑定问卷')
    status=models.BooleanField(default=True)


#老师
class Teacher(models.Model):
    user=models.OneToOneField(to='Users',on_delete=models.CASCADE,help_text='绑定用户')
    is_valied=models.BooleanField(default=False)
    re_password=models.BooleanField(default=False)

    def __str__(self):
        return self.user.name

# ---------------------------------------------------------------------------- U


#用户表

class Users(AbstractUser):
    username=models.CharField(max_length=20,unique=True,help_text='账户名')
    name=models.CharField(max_length=20,help_text='账户名',default='xx')
    mobile=models.CharField(max_length=15,help_text='手机号',unique=True)
    age=models.IntegerField(help_text='年龄',default=0)
    sex=models.CharField(choices=(('男','男'),('女','女'),('未知','未知')),max_length=5,help_text='性别',default='未知')
    e_maile=models.EmailField(null=True,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    password=models.CharField(max_length=50,help_text='密码')
    def __str__(self):
        return self.name


#用户角色
class UsersRoles(models.Model):
    user=models.ForeignKey(to='Users',on_delete=models.CASCADE,related_name='userrole')
    role=models.ForeignKey(to='Roles',on_delete=models.CASCADE)
    # created_at=models.DateTimeField(auto_now_add=True)
    # updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        unique_together=('user','role')
    def __str__(self):
        return '{}|{}'.format(self.user.username,self.role.role)


# ---------------------------------------------------------------------------- V
# ---------------------------------------------------------------------------- W


#注册老师等待发送的消息
class WaitSend(models.Model):
    create_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(to='Users',on_delete=models.CASCADE)
    content=models.TextField(help_text='在这里输入需要发送的内容')
    choices=(
        (1,'批量注册老师'),
        (2,'家长问卷通知'),
        (3,'其他类型的通知'),
    )
    content_type=models.CharField(choices=choices,max_length=10)
    remark=models.TextField(help_text='在这里输入帮助信息')
    status=models.BooleanField(default=True)


#学生短信等待发送
class WaitSendStudentSmS(models.Model):
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    student_obj=models.ForeignKey(to='Student',on_delete=models.CASCADE)
    questionnaire_obj=models.ForeignKey(to='Questionnaire',on_delete=models.CASCADE)
    content=models.TextField()
    success_status=models.BooleanField(default=True)
    def __str__(self):
        return '学生名字：{}<br>手机号码：{}<br>内容：{}<br>'.\
            format(self.student_obj.user.username,self.student_obj.user.mobile,self.content,)




# ---------------------------------------------------------------------------- X
# ---------------------------------------------------------------------------- Y
# ---------------------------------------------------------------------------- Z

















# ---------------------------------------------------------------------------- A
# ---------------------------------------------------------------------------- B
# ---------------------------------------------------------------------------- C
# ---------------------------------------------------------------------------- D
# ---------------------------------------------------------------------------- E
# ---------------------------------------------------------------------------- F
# ---------------------------------------------------------------------------- G
# ---------------------------------------------------------------------------- H
# ---------------------------------------------------------------------------- I
# ---------------------------------------------------------------------------- J
# ---------------------------------------------------------------------------- K
# ---------------------------------------------------------------------------- L
# ---------------------------------------------------------------------------- M
# ---------------------------------------------------------------------------- N
# ---------------------------------------------------------------------------- O
# ---------------------------------------------------------------------------- P
# ---------------------------------------------------------------------------- Q
# ---------------------------------------------------------------------------- R
# ---------------------------------------------------------------------------- S
# ---------------------------------------------------------------------------- T
# ---------------------------------------------------------------------------- U
# ---------------------------------------------------------------------------- V
# ---------------------------------------------------------------------------- W
# ---------------------------------------------------------------------------- X
# ---------------------------------------------------------------------------- Y
# ---------------------------------------------------------------------------- Z




