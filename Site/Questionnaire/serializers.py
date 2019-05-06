from rest_framework import serializers
from .models import *
import time,openpyxl,datetime,random,os
from Tools.tools import get_user_role,SendSMS,get_utc_now,raise_error
from django.conf import settings
#这个字段不用填了


class chatserializer(serializers.ModelSerializer):
    class Meta:
        model=chat
        fields=('created_at','centext',)


def get_query(model,field=None,kwargs=None):
    '''
    为序列化器的ChoiceField类型字段的choices参数提供可选值
    :param model:模型类
    :param field:用于生成返回值的help变量/为None时使用实例__str__方法的返回值作为help
    :param kwargs:结果集筛选条件
    :return:[(id,help),(id,help),...]
    '''
    if not kwargs:
        objs=model.objects.all()
    else:
        objs = model.objects.filter(**kwargs)
    if field:
        return [(obj.id,getattr(obj,field)) for obj in objs]
    else:
        return [(obj.id, str(obj)) for obj in objs]

# ---------------------------------------------------------------------------- A

#动作
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Action
        fields=('id','action','help')


# ---------------------------------------------------------------------------- B


#批量注册学生
class BatchStudentSerializer(serializers.Serializer):

    def __new__(cls,*args,**kwargs):
        data=kwargs.get('data',None)
        class_obj=data.pop('class_obj') if data else None
        obj=super().__new__(cls,*args,**kwargs)
        obj.class_obj=class_obj
        return obj
    file=serializers.FileField(help_text='选择一个excel表格文件[支持的格式]')

    #1.对上传的文件进行解析并验证
    def validate_file(self, file):

        path='files/{}_{}'.format(time.time(),file.name)
        with open(path,'wb') as f:
            for i in file.chunks():
               f.write(i)
        wb = openpyxl.load_workbook(path)
        try:
            sheet=wb.get_sheet_by_name('批量注册')
        except:
            raise serializers.ValidationError('在本文件中没有发现名为[批量注册]的sheet.')
        h, l = sheet.max_row, sheet.max_column
        lines=sheet['A1':'{}{}'.format(chr(ord('A')+l-1),h)]
        datas=[]
        for line in lines:
            infos=[cell.value for cell in line]
            datas.append(infos)

        field_info=datas[0]
        body_info=datas[1:]

        field_info =self.my_validate_field_info(field_info)
        self.my_validate_body_info(field_info,body_info)
        return field_info, body_info

    #1-1.验证表格的标题部分/转化为携带下标的字典
    def my_validate_field_info(self, field_info):
        allow_field={'学生姓名':'name','手机号':'mobile',}
        field_info_dict={}
        for index,field in enumerate(field_info):
            if field not in allow_field:
                raise serializers.ValidationError('提供了多余的字段:{}'.format(field))
            else:
                field_info[index]=allow_field[field]
                field_info_dict[allow_field[field]]=index
        #返回样式{'name': 0, 'mobile': 1,}
        return field_info_dict

    #1-2.验证表格的内容部分
    def my_validate_body_info(self,field_info,body_info):

        errors=[]
        self.save_list = []
        for index,student_info in enumerate(body_info):
            data={}
            for field in field_info:
                data[field]=student_info[field_info[field]]
            data_info=data.copy()
            error=self.my_validate_student(data)
            if error :
                info='第{}行[{}]未能通过验证---><br>{}'.format(str(index+1),data_info,' '*16)
                errors.append(info+str(error))
        if errors:
            raise serializers.ValidationError(errors)

    #1-2-1.验证单条数据
    def my_validate_student(self,data):
        # 班级信息 学生信息
        class_obj=self.class_obj
        data['class_id']=class_obj.id
        data['password']=self.get_random_password()
        # name mobile password class_id
        serializer=RegStudentSerializer(data=data)
        if serializer.is_valid():
            self.save_list.append(serializer)
            return None
        else:
            return serializer.errors

    def get_random_password(self):
        password=[str(random.randint(0,9)) for i in range(10)]
        password=''.join(password)
        return password

    #2.创建这些学生用户
    def create(self,*args,**kwargs):
        self.success_info=[]
        for save in self.save_list:
            save.save()
            student_obj=Student.objects.filter(user=save.instance).first()
            serializer=StudentSerializer(student_obj)
            self.success_info.append(serializer.data)
        return True


#批量注册老师
class BatchTeacherSerializer(serializers.Serializer):
    file=serializers.FileField(help_text='选择一个excel表格文件[支持的格式]')
    #1.对上传的文件进行解析并验证
    def validate_file(self, file):
        path='files/{}_{}'.format(time.time(),file.name)
        with open(path,'wb') as f:
            for i in file.chunks():
               f.write(i)
        wb = openpyxl.load_workbook(path)
        try:
            sheet=wb.get_sheet_by_name('批量注册')
        except:
            raise serializers.ValidationError('在本文件中没有发现名为[批量注册]的sheet.')
        h, l = sheet.max_row, sheet.max_column
        lines=sheet['A1':'{}{}'.format(chr(ord('A')+l-1),h)]
        datas=[]
        for line in lines:
            infos=[cell.value for cell in line]
            datas.append(infos)
        field_info=datas[0]
        body_info=datas[1:]
        field_info =self.my_validate_field_info(field_info)
        self.my_validate_body_info(field_info,body_info)
        return field_info, body_info

    #1-1.验证表格的标题部分/转化为携带下标的字典
    def my_validate_field_info(self, field_info):
        allow_field={'老师姓名':'name','手机号':'mobile','初始密码':'password',
                     '学校':'school','年级':'grade','班级':'class_name',}
        field_info_dict={}
        for index,field in enumerate(field_info):
            if field not in allow_field:
                raise serializers.ValidationError('提供了多余的字段:{}'.format(field))
            else:
                field_info[index]=allow_field[field]
                field_info_dict[allow_field[field]]=index
        #返回样式{'name': 0, 'mobile': 1, 'password': 2, 'school': 3, 'grade': 4, 'class_name': 5}
        return field_info_dict

    #1-2.验证表格的内容部分
    def my_validate_body_info(self,field_info,body_info):

        errors=[]
        self.save_list = []
        for index,teacher_info in enumerate(body_info):
            data={}
            for field in field_info:
                data[field]=teacher_info[field_info[field]]
            data_info=data.copy()
            error=self.my_validate_teacher(data)
            if error :
                info='第{}行[{}]未能通过验证---><br>{}'.format(str(index+1),data_info,' '*16)
                errors.append(info+str(error))
        if errors:
            raise serializers.ValidationError(errors)

    #1-2-1.验证单条数据
    def my_validate_teacher(self,data):
        # 班级信息 老师信息
        school_info = data.pop('school')
        grade_info = data.pop('grade')
        class_name_info = data.pop('class_name')
        filter_data={'class_name__contains':class_name_info,
         'gradeclass__grade__grade_name__contains':grade_info,
           'gradeclass__grade__schoolgrade__school__school_name__contains':school_info}
        class_obj=Class.objects.filter(**filter_data)
        if len(class_obj)==1:
            class_id=class_obj.first().id
        elif not class_obj:
            return '表格提供的信息未能定位到班级[请检查学校/年级/班级是否已经存在]<br>'
        else:
            return '此参数条件下查找到符合条件的多个班级.请保证学校/年级/班级信息完整无误<br>'
        data['class_id']=class_id
        data['is_valied']=True
        # 'name', 'mobile', 'password', 'class_id', 'is_valied',
        serializer=RegTeacherSerializer(data=data)
        if serializer.is_valid():
            self.save_list.append([serializer,data])
            return None
        else:
            return serializer.errors

    #2.创建这些老师用户
    def create(self,*args,**kwargs):
        self.success_info=[]
        for serializer,data in self.save_list:
            serializer.save()
            teacher_obj=Teacher.objects.filter(user=serializer.instance).first()
            serializer2=TeacherSerializer(teacher_obj)
            # user_id=teacher_obj.user.id
            password=data.get('password')
            user_name=teacher_obj.user.name
            url='118.25.213.122:8889/index'
            content=settings.BEATCHTEACHERSMS.format(user_name,password,url)
            mobile=data.get('mobile')
            sms=SendSMS(mobile=mobile,data=content)
            temp='成功' if sms.send() else '失败'
            data=dict(serializer2.data)
            data['sms']=temp
            self.success_info.append(data)
        return True


#批量的向班级发送问卷--读
class BatchClassQuestionnaireReadSerializer(serializers.ModelSerializer):
    school = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    school_id=serializers.SerializerMethodField()
    grade_id=serializers.SerializerMethodField()

    def get_school(self, obj):
        school_obj = School.objects.filter(schoolgrade__grade__gradeclass__class_name=obj).first()
        return school_obj.school_name

    def get_grade(self, obj):
        grade_obj = Grade.objects.filter(gradeclass__class_name=obj).first()
        return grade_obj.grade_name

    def get_school_id(self, obj):
        school_obj = School.objects.filter(schoolgrade__grade__gradeclass__class_name=obj).first()
        return school_obj.id

    def get_grade_id(self, obj):
        grade_obj = Grade.objects.filter(gradeclass__class_name=obj).first()
        return grade_obj.id

    questionnaire_id=serializers.ChoiceField(write_only=True,choices=#((1,2,),(3,4,)))
        (lambda :[(obj.id,obj.questionnaire_name)
            for obj in Questionnaire.objects.get_queryset().order_by('create_at')])())

    class Meta:
        model=Class
        fields=('id','class_name','school','grade','questionnaire_id',
                'school_id','grade_id',)
        read_only_fields=('class_name',)


#批量的向班级发送问卷--写
class BatchClassQuestionnaireWriteSerializer(serializers.Serializer):
    school = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()

    def get_school(self, obj):
        school_obj = School.objects.filter(schoolgrade__grade__gradeclass__class_name=obj).first()
        return school_obj.school_name

    def get_grade(self, obj):
        grade_obj = Grade.objects.filter(gradeclass__class_name=obj).first()
        return grade_obj.grade_name

    def __init__(self,*args,**kwargs):
        self.queryset=kwargs.pop('queryset')
        super().__init__(*args,**kwargs)
    questionnaire_id=serializers.CharField(write_only=True)

    class Meta:
        model=ClassQuestionnaire
        fields=('id','questionnaire_id','school','grade',)

    def create(self,data):
        #保存成功后把成功信息保存进这里,供视图使用
        self.success_info = []
        for serializer in self.serializers:
            serializer.save()
            self.success_info.append(serializer.data)
        return self.success_info

    def validate(self, data):
        self.serializers = []
        questionnaire_id = data.get('questionnaire_id')
        #对班级的集合进行逐个验证
        for obj in self.queryset:
            data={'class_obj':obj.id,'questionnaire_obj':questionnaire_id}
            serializer=ClassQuestionnaireSerializer(data=data)
            if serializer.is_valid():
                self.serializers.append(serializer)
            else:
                grade_obj=obj.gradeclass.grade
                school_name=grade_obj.schoolgrade.school.school_name
                grade_name=grade_obj.grade_name
                class_name=obj.class_name
                args=(school_name,grade_name,class_name,questionnaire_id)
                info='错误位置：学校[{}]年级[{}]班级[{}]问卷[{}]'.format(*args)
                raise serializers.ValidationError(info+str(serializer.errors))
        return data

    def validate_questionnaire_id(self, attrs):
        if Questionnaire.objects.filter(pk=attrs):
           return attrs
        else:
            raise serializers.ValidationError('通过这个问卷的id没有定位到问卷,请检查后再试')


#批量的向学生发送问卷
class BatchStudentQuestionnaireSerializer(serializers.ModelSerializer):
    def __new__(cls,*args,**kwargs):
        view=kwargs.get('context').get('view')

        user =view.request.user
        if user:
            #定位老师
            teacher_objs=Teacher.objects.filter(user=user)
            #定位班级
            class_objs=Class.objects.filter(classteacher__teacher__in=teacher_objs)
            #定位问卷
            questionnaires=Questionnaire.objects.filter(classquestionnaire__class_obj__in=class_objs)
            #获得可用的问卷id和名称
            for questionnaire in questionnaires:
                option=(questionnaire.id,questionnaire.questionnaire_name)
                cls.choices.append(option)
        obj=super().__new__(cls,*args,**kwargs)
        obj.view=view
        return obj

    choices = []
    student_name=serializers.CharField(source='user.name',read_only=True)
    school_name=serializers.SerializerMethodField()
    grade_name=serializers.SerializerMethodField()
    class_name=serializers.SerializerMethodField()
    questionnaires=serializers.SerializerMethodField()
    questionnaire_id=serializers.ChoiceField(choices=choices,write_only=True)


    class Meta:
        model=Student
        fields=('id','student_name','school_name','grade_name','class_name','questionnaires',
                'questionnaire_id',)

    #这个学生所在的学校
    def get_school_name(self,obj):
        school=School.objects.filter\
            (schoolgrade__grade__gradeclass__class_name__classstudent__student=obj).first()
        return school.school_name if school else ''
    #这个学生所在的年级
    def get_grade_name(self,obj):
        grade=Grade.objects.filter\
            (gradeclass__class_name__classstudent__student=obj).first()
        return grade.grade_name if grade else ''
    #这个学生所在的班级
    def get_class_name(self,obj):
        class_obj=Class.objects.filter\
            (classstudent__student=obj).first()
        return class_obj.class_name if class_obj else ''
    #这个学生拥有的问卷
    def get_questionnaires(self,obj):
        studentquestionnaire=StudentQuestionnaire.objects.filter(student_obj=obj)
        questionnaire =[s_q_obj.questionnaire_obj.questionnaire_name for s_q_obj
                        in studentquestionnaire]
        return questionnaire

    #验证信息
    def validate(self,data):
        questionnaire_obj_id = data.get('questionnaire_id')
        self.serializers=[]

        for student_obj in self.view.get_queryset():
            data = {'questionnaire_obj': questionnaire_obj_id,
                    'student_obj': student_obj.id,'view':self.view}
            serializer = StudentQuestionnaireSerializer(data=data)

            if serializer.is_valid():
                self.serializers.append(serializer)
            else:
                questionnaire_name=Questionnaire.objects.filter(pk=questionnaire_obj_id).first()
                info_args=(student_obj.user.name,questionnaire_name,serializer.errors)
                error='在为{}同学添加{}问卷时发生错误：{}'.format(*info_args)
                raise serializers.ValidationError(error)
        return data

    #开始批量的为学生添加问卷
    def create(self, validated_data):
        self.success_info=[]
        for serializer in self.serializers:
            serializer.save()
            sq_obj=serializer.instance
            #学生对象
            student_obj=sq_obj.student_obj
            #问卷对象
            questionnaire_obj=sq_obj.questionnaire_obj
            #创建时间created_at
            #更新时间updated_at
            #短信内容
            student_name=student_obj.user.name
            questionnaire_url=questionnaire_obj.questionnaire_url
            content='您有一份关于您的孩子{}同学的问卷等待被填写。问卷链接：{}'.format(student_name,questionnaire_url)
            #保存
            sms_data={'student_obj':student_obj.id,'questionnaire_obj':questionnaire_obj.id,'content':content}
            sms_serializer=WaitSendStudentSmSSerializer(data=sms_data)
            if sms_serializer.is_valid():
                sms_serializer.save()
                sms_serializer.sms_send()

            self.success_info.append(serializer.data)
        return Student.objects.filter().first()


# ---------------------------------------------------------------------------- C


#城市
class CitySerializer(serializers.ModelSerializer):
    province_name=serializers.CharField(source='province_obj.province_name',read_only=True)
    class Meta:
        model=City
        fields=('id','province_name','city_name','create_at','province_obj',)


#城市学校关联表
class CitySchoolSerialzier(serializers.ModelSerializer):
    city_name=serializers.CharField(source='city_obj.city_name',read_only=True)
    school_name=serializers.CharField(source='school_obj.school_name',read_only=True)
    class Meta:
        model=CitySchool
        fields=('id','city_obj','school_obj','city_name','school_name',)


#绑定学生与班级
class ClassStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ClassStudent
        fields=('id','s_class','student',)


#绑定老师与班级
class ClassTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=ClassTeacher
        fields=('id','teacher','class_name',)


#班级
class ClassSerializer(serializers.ModelSerializer):
    school=serializers.SerializerMethodField()
    grade=serializers.SerializerMethodField()
    teacher=serializers.SerializerMethodField()
    grade_id=serializers.ChoiceField(choices=get_query(model=Grade),write_only=True)
    questionnaire=serializers.SerializerMethodField()

    def validate(self, attrs):
        grade_id=attrs.get('grade_id')
        class_name=attrs.get('class_name')
        if GradeClass.objects.filter(grade__id=grade_id,class_name__class_name=class_name):
            raise serializers.ValidationError('这个年级已经存在{}'.format(class_name))
        return attrs


    def get_school(self,obj):
        school_obj = School.objects.filter(schoolgrade__grade__gradeclass__class_name=obj).first()
        if school_obj:
            return school_obj.school_name
        else:
            return '没有查找到学校'

    def get_grade(self,obj):
        grade_obj = Grade.objects.filter(gradeclass__class_name=obj).first()
        return grade_obj.grade_name if grade_obj else '没有找到对应的年级'

    def get_teacher(self,obj):
        teacher_objs=Teacher.objects.filter(classteacher__class_name=obj)
        return ['老师姓名：{}----老师id：{}'.format(teacher_obj.user.name,teacher_obj.user.id)
                for teacher_obj in teacher_objs]

    def get_questionnaire(self,obj):
        questionnaire_objs=Questionnaire.objects.filter(classquestionnaire__class_obj=obj)
        return ['问卷名：{}-----问卷id：{}'.format(questionnaire_obj.questionnaire_name,questionnaire_obj.id)
                for questionnaire_obj in questionnaire_objs]

    class Meta:
        model=Class
        fields=('id','class_name','school','grade','teacher',
                'grade_id','questionnaire',)


    def create(self,data):
        #创造班级
        class_name=data.get('class_name')
        class_obj=super().create({'class_name':class_name})
        #绑定年级
        grade_id=data.get('grade_id')
        class_id=class_obj.id
        serializer=GradeClassSerializer(data={'grade':grade_id,'class_name':class_id})
        if serializer.is_valid():
            serializer.save()
            return class_obj
        else:
            raise serializers.ValidationError(serializer.errors)


#验证码
class CodesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Codes
        fields=('id','mobile','created_at','type',)

    def get_code(self):
        return ''.join([str(random.randint(0,9)) for i in range(4)])

    def validate(self,data):
        mobile=data.get('mobile')
        now=get_utc_now()
        code_objs=Codes.objects.filter(mobile=mobile)
        if code_objs:
            if code_objs.filter(created_at__gt=now-settings.RE_CODE_TIME):
                raise serializers.ValidationError('这个手机号距离上次请求的时间还没有超过1分钟[开发期暂为5秒],请稍后再试')
        the_type=data.get('type')
        user=Users.objects.filter(mobile=mobile).first()
        #1为注册验证
        if the_type==1:
            if user:
                raise serializers.ValidationError('手机号已经被注册,请更换手机号注册')
            self.info_data='欢迎注册瓦力工厂，您的验证码为{}'
        # 2为改密验证
        elif the_type==2:
            if not user:
                raise serializers.ValidationError('手机号不存在,请检查输入是否正确')
            self.info_data='您正在修改瓦力工厂网站登陆密码，验证码为{}'
        else:
            raise serializers.ValidationError('不能识别的验证码类型')
        return {'mobile':mobile,'type':the_type}

    def create(self, validated_data):
        mobile=validated_data.get('mobile')
        code=self.get_code()
        validated_data['code']=code
        data=self.info_data.format(code)
        sms=SendSMS(mobile=mobile,data=data)
        status=sms.send()
        if status:
            code_obj=Codes.objects.create(**validated_data)
        else:
            raise serializers.ValidationError('发送失败')
        return code_obj


#班级问卷绑定
class ClassQuestionnaireSerializer(serializers.ModelSerializer):
    class_name=serializers.CharField(source='class_obj.class_name',read_only=True)
    questionnaire_obj_name=serializers.CharField(
        source='questionnaire_obj.questionnaire_name',read_only=True)
    class Meta:
        model=ClassQuestionnaire
        fields=('id','class_obj','questionnaire_obj','class_name','questionnaire_obj_name',)


# 城市添加城市负责人
class CityCityHeadSerializer(serializers.ModelSerializer):
    filter_kwargs={'userrole__role__role':settings.CITYHEAD}
    city_head_obj=serializers.ChoiceField(choices=get_query(model=Users,kwargs=filter_kwargs),
                                          write_only=True)
    city_head_mobile=serializers.SerializerMethodField(read_only=True)
    city_head_name=serializers.SerializerMethodField()
    city_head_id=serializers.SerializerMethodField()
    city_name=serializers.SerializerMethodField()


    def get_city_head_name(self,obj):
        return obj.city_head_obj.name

    def get_city_head_mobile(self,obj):
        return obj.city_head_obj.mobile


    def get_city_head_id(self,obj):
        return obj.city_head_obj.id

    def get_city_name(self,obj):
        return obj.city_obj.city_name




    def validate_city_head_obj(self, attrs):
        user=Users.objects.get(pk=attrs)
        return user

    class Meta:
        model=CityCityHead
        fields=('city_name','city_head_name',
            'id','city_obj','city_head_obj','city_head_id','city_head_mobile',)


# ---------------------------------------------------------------------------- D
# ---------------------------------------------------------------------------- E


#问卷被错误提交
class ErrorCommitSerializer(serializers.ModelSerializer):
    match_students=serializers.SerializerMethodField()
    match_studentquestionnaire=serializers.SerializerMethodField()
    class Meta:
        model=ErrorCommit
        fields=('id','create_at','original_name','original_school','original_grade','original_class',
                'original_code','error_type','error_help',
                'match_students','match_studentquestionnaire',)

    #提交错误但是匹配到了以下用户
    def get_match_students(self,obj):
        matchbuterror_objs=MatchButError.objects.filter(matcherrorcommit_obj=obj)
        if matchbuterror_objs:
            return [StudentSerializer(matchbuterror_obj.matchstudent_obj).data
                    for matchbuterror_obj in matchbuterror_objs]
        else:
            return ''

    #提交错误但是匹配到了以下问卷任务
    def get_match_studentquestionnaire(self,obj):
        matchbuterror_objs=MatchButError.objects.filter(matcherrorcommit_obj=obj)
        if matchbuterror_objs:
            return [StudentQuestionnaireSerializer(matchbuterror_obj.matchstudentquestionnaire_obj).data
                    for matchbuterror_obj in matchbuterror_objs]
        else:
            return ''

# ---------------------------------------------------------------------------- F
# ---------------------------------------------------------------------------- G


#年级班级绑定
class GradeClassSerializer(serializers.ModelSerializer):
    class Meta:
        model=GradeClass
        fields=('id','grade','class_name',)


#年级
class GradeSerializer(serializers.ModelSerializer):
    school=serializers.SerializerMethodField()
    school_id=serializers.ChoiceField(choices=get_query(model=School,field='school_name'),write_only=True)
    class Meta:
        model=Grade
        fields=('id','grade_name','school','school_id')
    def get_school(self,obj):
        school_obj=School.objects.filter(schoolgrade__grade=obj).first()
        if school_obj:
            return school_obj.school_name
        else:
            '没有找到关联的学校'
    def validate(self, attrs):
        grade_name = attrs.get('grade_name')
        school_id = attrs.get('school_id')
        if SchoolGrade.objects.filter(grade__grade_name=grade_name,school__id=school_id):
            raise serializers.ValidationError('这个学校已经存在这个班级')
        return attrs

    def create(self,data):
        #添加年级
        grade_name=data.get('grade_name')
        grade_obj=super().create({'grade_name':grade_name})
        grade_id=grade_obj.id
        #关联学校年级
        school_id=data.get('school_id')
        serializer=SchoolGradeSerializer(data={'school':school_id,'grade':grade_id})
        print('即将新建')
        if serializer.is_valid():
            print('有效')
            serializer.save()
            print()
            return grade_obj
        else:
            print('筹措了')
            raise Exception(serializer.errors)


#年级添加年级主任
class GradeGradeHeadSerializer(serializers.ModelSerializer):
    filter_kwargs={'userrole__role__role':settings.GRADEHEAD}#角色只能为年级主任
    grade_head_obj=serializers.ChoiceField(choices=get_query(model=Users,kwargs=filter_kwargs),
                                              write_only=True)
    school_name=serializers.SerializerMethodField(read_only=True)
    grade_name=serializers.SerializerMethodField(read_only=True)
    grade_head_name=serializers.SerializerMethodField(read_only=True)

    def get_school_name(self,obj):
        school=School.objects.filter(schoolgrade__grade__gradegradehead=obj).first()
        return school.school_name

    def get_grade_name(self,obj):
        return obj.grade_obj.grade_name

    def get_grade_head_name(self,obj):
        return obj.grade_head_obj.name

    #学校年级/名字/角色
    def validate_grade_head_obj(self, attrs):
        user=Users.objects.get(pk=attrs)
        return user

    class Meta:
        model=GradeGradeHead
        fields=('id','grade_obj','grade_head_obj','school_name','grade_name','grade_head_name',)


#省添加省负责人
class ProvinceProvinceHeadSerializer(serializers.ModelSerializer):
    filter_kwargs={'userrole__role__role':settings.BIGHEAD}
    province_head_obj=serializers.ChoiceField(choices=get_query(model=Users,
                                                 kwargs=filter_kwargs),write_only=True)

    province_head_name=serializers.SerializerMethodField(read_only=True)
    province_head_id =serializers.SerializerMethodField(read_only=True)
    province_name=serializers.SerializerMethodField(read_only=True)

    def get_province_head_name(self,obj):
        return obj.province_head_obj.name

    def get_province_head_id(self,obj):
        return obj.province_head_obj.id

    def get_province_name(self,obj):
        return obj.province_obj.province_name

    def validate_province_head_obj(self, attrs):
        return Users.objects.get(pk=attrs)

    class Meta:
        model=ProvinceProvinceHead
        fields=('id','province_head_name','province_name',
                'province_obj','province_head_obj','province_head_id',)






# ---------------------------------------------------------------------------- H
# ---------------------------------------------------------------------------- I
# ---------------------------------------------------------------------------- J
# ---------------------------------------------------------------------------- K
# ---------------------------------------------------------------------------- L


#登陆
class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        mobile=data.get('mobile')
        password=data.get('password')
        if not mobile or not password:
            raise serializers.ValidationError('[name]及[password]是必填的字段')
        user=Users.objects.filter(mobile=mobile).first()

        if not user:
            raise serializers.ValidationError('用户不存在,检查手机号')
        status=user.check_password(password)
        self.user = user
        if status:
            return data
        else:
            raise serializers.ValidationError('手机号或者密码不正确')



# ---------------------------------------------------------------------------- M


#问卷虽然被错误提交,但成功匹配到了一个或者多个任务/学生,这个表记录这些匹配并与ErrorCommit关联
class MatchButErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model=MatchButError
        fields=('matchstudent_obj','matchstudentquestionnaire_obj','matcherrorcommit_obj',)


# ---------------------------------------------------------------------------- N
# ---------------------------------------------------------------------------- O
# ---------------------------------------------------------------------------- P


#省
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Province
        fields=('id','create_at','province_name',)



# ---------------------------------------------------------------------------- Q


#问卷类型
class QuestionnaireTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=QuestionnaireType
        fields=('id','type_name','help',)


#问卷
class QuestionnaireSerializer(serializers.ModelSerializer):
    questionnaire_type_name=serializers.CharField(source='questionnaire_type.type_name',
                                                  read_only=True)
    questionnaire_code=serializers.CharField(read_only=True)

    class Meta:
        model=Questionnaire
        fields=('id','questionnaire_url','questionnaire_name','questionnaire_type',
                'grade_name_field','class_name_field','student_name_field',
                'questionnaire_type_name',
                'questionnaire_code',)

    def create(self, validated_data):
        url=validated_data.get('questionnaire_url')
        code=url.split('/')[-1]
        code=code.strip()
        validated_data['questionnaire_code']=code
        return super().create(validated_data)


#金数据向服务器发送问卷答题数据.解析数据及更新任务状态
class QuestionnaireMediaSerializer(serializers.Serializer):
    form=serializers.CharField(write_only=True)
    form_name=serializers.CharField(write_only=True)

    def validate(self, attrs):
        # 解析数据
        form = attrs.get('form')
        self.form=form
        # 1.定位问卷
        questionnaire_obj=self.custom_get_questionnaire_obj(form)
        if not questionnaire_obj:
            self.cue_handler = \
                self.no_questionnaire_handler
            return super().validate(attrs)
        self.questionnaire_obj=questionnaire_obj
        #2.找到学校年级班级所对应的字段.这些信息都记录在问卷表里.
        grade_field,class_field,student_field= \
            self.custom_get_school_grade_class_field(questionnaire_obj)
        entry = self.initial_data.get('entry')
        # school_name=entry.get(school_field)
        # self.school_name=school_name
        grade_name=entry.get(grade_field)
        self.grade_name=grade_name
        class_name=entry.get(class_field)
        self.class_name=class_name
        student_name=entry.get(student_field)
        self.student_name=student_name
        # 3.定位参与者
        student_objs=self.custom_get_student_obj(grade_name, class_name, student_name)
        self.student_objs=student_objs
        # 4.定位任务
        self.studentquestionnaire_obj=self.custom_get_studentquestionnaire_obj()
        # 5.根据不同的情况选择处理程序
        self.cue_handler= \
            self.custom_get_cue_handler()
        return super().validate(attrs)

    def create(self, validated_data):
        # self.success_info={'xxoo':'ooxx'}
        self.success_info =self.cue_handler()
        return {}

    # 1.定位问卷
    def custom_get_questionnaire_obj(self,form):
        questionnaire_obj = Questionnaire.objects.filter(questionnaire_code=form).first()
        self.questionnaire_obj=questionnaire_obj
        print('找到问卷-->',questionnaire_obj.questionnaire_name)
        return questionnaire_obj

    # 2.找到学校年级班级所对应的字段.这些信息都记录在问卷表里.
    def custom_get_school_grade_class_field(self,questionnaire_obj):
        # school_field='field_{}'.format(str(questionnaire_obj.school_name_field))
        grade_field='field_{}'.format(str(questionnaire_obj.grade_name_field))
        class_field= 'field_{}'.format(str(questionnaire_obj.class_name_field))
        student_field= 'field_{}'.format(str(questionnaire_obj.student_name_field))
        return grade_field,class_field,student_field

    # 3.定位参与者
    def custom_get_student_obj(self,grade_name,class_name,student_name):
        #去掉两边空格
        options=[]
        for option in [grade_name,class_name,student_name]:
            option=option.strip()
            options.append(option)
        grade_name, class_name, student_name=options
        grade_list=self.custom_get_grade_list(grade_name)
        class_list=self.custom_get_class_list(class_name)
        student_kwargs={
            # 'classstudent__s_class__gradeclass__grade__schoolgrade__school__school_name__contains':
            #     school_name,
            # 'classstudent__s_class__gradeclass__grade__grade_name__contains':grade_name,
            'classstudent__s_class__gradeclass__grade__in': grade_list,
            # 'classstudent__s_class__class_name__contains':class_name,
            'classstudent__s_class__in': class_list,
            'user__name':student_name
        }
        student_objs=Student.objects.filter(**student_kwargs)
        self.student_objs=student_objs
        return student_objs

    # 4.定位任务
    def custom_get_studentquestionnaire_obj(self):
        if self.questionnaire_obj:
            student_obj=self.student_objs.first()
            questionnaire_obj=self.questionnaire_obj
            studentquestionnaire_obj=StudentQuestionnaire.objects.filter(student_obj=student_obj,
                                                questionnaire_obj=questionnaire_obj).first()
            return studentquestionnaire_obj
        else:
            return None

    # 5.根据不同的情况选择处理程序
    def custom_get_cue_handler(self):
        '''
        根据定位到的学生集指定处理程序
        '''
        questionnaire_obj = self.questionnaire_obj
        # 问卷不存在/此问卷没有被注册
        if not questionnaire_obj:
            return self.no_questionnaire_handler
        student_objs=self.student_objs
        #没有定位到学生
        if not student_objs:
            #提交者提交的信息不能查询到这个学生[可能信息填写有误]handler
            cue_handler=self.no_student_handler
        #只定位到一个学生
        elif len(student_objs)==1:
            #执行定位任务
            studentquestionnaire_obj =self.custom_get_studentquestionnaire_obj()
            self.studentquestionnaire_obj=studentquestionnaire_obj
            #没有定位到任务
            if not studentquestionnaire_obj:
                #提交者属于学校的学生但是未被邀请填写问卷handler
                cue_handler =self.not_invited_handler
            # 成功定位到任务
            else:
                if studentquestionnaire_obj.status:
                    #问卷进行中  成功找到了提交者及任务handler
                    cue_handler = self.status_true_handler
                else:
                    #问卷已关闭  提交者进行了重复提交handler
                    cue_handler = self.status_false_handler
        # 匹配到多个学生
        else:
            # 匹配到多个学生handler
            cue_handler = self.many_student_handler
        return cue_handler

    # +*提交处理程序(成功匹配)----成功定位了任务/更新这个任务的状态
    def status_true_handler(self):
        self.studentquestionnaire_obj.status=False
        self.studentquestionnaire_obj.save()
        serializer=StudentQuestionnaireSerializer(self.studentquestionnaire_obj)
        return serializer.data

    # +*提交处理程序(错误类型1)----提交者提交的信息不能查询到这个学生
    def no_student_handler(self):
        # 制作原始数据
        original_school =self.school_name
        original_grade =self.grade_name
        original_class =self.class_name
        original_name =self.student_name
        original_code =self.form
        # 问卷里提供的信息不足以查询到这个学生
        error_type = 1
        # 制作错误信息
        error_help='提交者提交的数据没有匹配到用户.'
        data={'original_school':original_school,'original_grade':original_grade,
              'original_class':original_class,'original_name':original_name,
              'original_code':original_code,'error_type':error_type,'error_help':error_help}
        # 写入错误提交数据表--原始数据--序列化并保存
        serializer=ErrorCommitSerializer(data=data)
        if serializer.is_valid():
            self.errorcommit_obj=serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)
        # 返回错误提交数据表的数据
        error_serializer=ErrorCommitSerializer(self.errorcommit_obj)
        return error_serializer.data

    # +*提交处理程序(错误类型2)----提交者属于学校的学生但是未被邀请填写问卷
    def not_invited_handler(self):
        # 制作原始数据
        original_school =self.school_name
        original_grade =self.grade_name
        original_class =self.class_name
        original_name =self.student_name
        original_code =self.form
        # 问卷里提供的信息不足以查询到这个学生
        error_type = 2
        # 制作错误信息
        error_help='提交者属于学校的学生但是未被邀请填写问卷.'
        data={'original_school':original_school,'original_grade':original_grade,
              'original_class':original_class,'original_name':original_name,
              'original_code':original_code,'error_type':error_type,'error_help':error_help}
        # 写入错误提交数据表--原始数据--序列化并保存
        serializer=ErrorCommitSerializer(data=data)
        if serializer.is_valid():
            self.errorcommit_obj=serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)
        #添加匹配学生
        #得到学生obj,问卷obj,原始数据obj
        matchstudent_obj=self.student_objs.first()
        matcherrorcommit_obj=self.errorcommit_obj
        data={'matchstudent_obj':matchstudent_obj.id,
              'matcherrorcommit_obj':matcherrorcommit_obj.id,}
        # 写入错误提交匹配表--匹配数据
        serializer=MatchButErrorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)

        error_serializer=ErrorCommitSerializer(self.errorcommit_obj)
        return error_serializer.data

    # +*提交处理程序(错误类型3)----成功定位了任务/但是这个任务已经关闭了
    def status_false_handler(self):
        # 制作原始数据
        original_name =self.student_name
        original_school =self.school_name
        original_grade =self.grade_name
        original_class =self.class_name
        original_code =self.form
        error_type = 3
        # 制作错误信息
        error_help='成功匹配到了参与者信息,并且匹配到参与者的问卷任务.但是这个任务已经关闭了.'\
            '可能的原因为:问卷已经提交过了或者问卷已经过期了或者问卷已经被人为的关闭了.'
        data={'original_school':original_school,'original_grade':original_grade,
              'original_class':original_class,'original_name':original_name,
              'original_code':original_code,'error_type':error_type,'error_help':error_help}
        # 写入错误提交数据表--原始数据
        serializer=ErrorCommitSerializer(data=data)
        if serializer.is_valid():
            self.errorcommit_obj=serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)


        #得到学生obj,问卷obj,原始数据obj
        matchstudent_obj=self.student_objs.first()
        matchstudentquestionnaire_obj=self.studentquestionnaire_obj
        matcherrorcommit_obj=self.errorcommit_obj
        data={'matchstudent_obj':matchstudent_obj.id,
              'matchstudentquestionnaire_obj':matchstudentquestionnaire_obj.id,
              'matcherrorcommit_obj':matcherrorcommit_obj.id,}
        # 写入错误提交匹配表--匹配数据
        serializer=MatchButErrorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)

        error_serializer=ErrorCommitSerializer(self.errorcommit_obj)
        return error_serializer.data

    # 匹配到多个学生,分流程序
    def many_student_handler(self):
        '''
        问卷已经证实存在,但是查找到多个学生
        '''
        questionnaire_obj=self.questionnaire_obj
        studentquestionnaire_objs=[]
        self.many_studentquestionnaire_objs=studentquestionnaire_objs
        for student_obj in self.student_objs:
            #定位任务
            studentquestionnaire_obj=StudentQuestionnaire.objects.filter(student_obj=student_obj,
                                                questionnaire_obj=questionnaire_obj).first()
            if studentquestionnaire_obj:
                studentquestionnaire_objs.append(studentquestionnaire_obj)
        #(错误类型6)----通过提交的信息查找到多个学生,但是所有的学生都没有被邀请
        if not studentquestionnaire_objs:
            return self.many_studeny_but_not_invited_handler
        #通过提交的信息匹配到多个学生,但是其中有且仅有一个学生成功匹配到任务
        elif len(studentquestionnaire_objs)==1:
            self.studentquestionnaire_obj=studentquestionnaire_objs[0]
            return self.status_true_handler
        #(错误类型4)----通过提交的信息查找到多个学生,但是其中多个学生都拥有这份问卷,系统不知道具体是哪一个问卷任务
        else:
            return self.many_studeny_many_questionnaire_handler()

    # 提交处理程序(错误类型4)----通过提交的信息查找到多个学生,但是其中多个学生都拥有这份问卷,系统不知道具体是哪一个问卷任务
    def many_studeny_many_questionnaire_handler(self):
        # 制作原始数据
        original_school =self.school_name
        original_grade =self.grade_name
        original_class =self.class_name
        original_name =self.student_name
        original_code =self.form
        # 问卷里提供的信息不足以查询到这个学生
        error_type = 4
        # 制作错误信息
        error_help='通过提交的信息查找到多个学生,但是其中多个学生都拥有这份问卷,系统不知道具体是哪一个问卷任务.'
        data={'original_school':original_school,'original_grade':original_grade,
              'original_class':original_class,'original_name':original_name,
              'original_code':original_code,'error_type':error_type,'error_help':error_help}
        # 写入错误提交数据表--原始数据--序列化并保存
        serializer=ErrorCommitSerializer(data=data)
        if serializer.is_valid():
            self.errorcommit_obj=serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)

        for studentquestionnaire_obj in self.many_studentquestionnaire_objs:
            #得到学生obj,问卷obj,原始数据obj
            matchstudent_obj=studentquestionnaire_obj.student_obj
            matchstudentquestionnaire_obj=studentquestionnaire_obj
            matcherrorcommit_obj=self.errorcommit_obj
            data={'matchstudent_obj':matchstudent_obj.id,
                  'matchstudentquestionnaire_obj':matchstudentquestionnaire_obj.id,
                  'matcherrorcommit_obj':matcherrorcommit_obj.id,}
            # 写入错误提交匹配表--匹配数据
            serializer=MatchButErrorSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise serializers.ValidationError(serializer.errors)
        error_serializer=ErrorCommitSerializer(self.errorcommit_obj)
        return error_serializer.data

    # +*提交处理程序(错误类型5)----此问卷没有在服务器注册,请及时注册,以免耽误正常业务.
    def no_questionnaire_handler(self):
        # 制作原始数据
        original_school ='问卷未注册无法找到学校所在字段'
        original_grade ='问卷未注册无法找到年级所在字段'
        original_class ='问卷未注册无法找到班级所在字段'
        original_name ='问卷未注册无法找到姓名所在字段'
        original_code =self.form
        # 问卷里提供的信息不足以查询到这个学生
        error_type = 5
        # 制作错误信息
        error_help='此问卷没有在服务器注册,请及时注册,以免耽误正常业务.'
        data={'original_school':original_school,'original_grade':original_grade,
              'original_class':original_class,'original_name':original_name,
              'original_code':original_code,'error_type':error_type,'error_help':error_help}
        # 写入错误提交数据表--原始数据--序列化并保存
        serializer=ErrorCommitSerializer(data=data)
        if serializer.is_valid():
            self.errorcommit_obj=serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)
        error_serializer=ErrorCommitSerializer(self.errorcommit_obj)
        return error_serializer.data

    # 提交处理程序(错误类型6)----通过提交的信息查找到多个学生,但是所有的学生都没有被邀请
    def many_studeny_but_not_invited_handler(self):
        # 制作原始数据
        original_school =self.school_name
        original_grade =self.grade_name
        original_class =self.class_name
        original_name =self.student_name
        original_code =self.form
        # 问卷里提供的信息不足以查询到这个学生
        error_type = 6
        # 制作错误信息
        error_help='通过提交的信息查找到多个学生,但是所有的学生都没有被邀请.'
        data={'original_school':original_school,'original_grade':original_grade,
              'original_class':original_class,'original_name':original_name,
              'original_code':original_code,'error_type':error_type,'error_help':error_help}
        # 写入错误提交数据表--原始数据--序列化并保存
        serializer=ErrorCommitSerializer(data=data)
        if serializer.is_valid():
            self.errorcommit_obj=serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)
        #获得学生集,依次写入错误关联表
        for student_obj in self.student_objs:
            #得到学生obj,问卷obj,原始数据obj
            matchstudent_obj=student_obj
            matcherrorcommit_obj=self.errorcommit_obj
            data={'matchstudent_obj':matchstudent_obj.id,
                  'matcherrorcommit_obj':matcherrorcommit_obj.id,}
            # 写入错误提交匹配表--匹配数据
            serializer=MatchButErrorSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise serializers.ValidationError(serializer.errors)
        error_serializer=ErrorCommitSerializer(self.errorcommit_obj)
        return error_serializer.data

    #通过关键字得到年级集合
    def custom_get_grade_list(self,grade_name):
        #以小写模式查找集合
        data=self.bignum_to_smallnum(grade_name)
        grade_list_small=Grade.objects.filter(grade_name__contains=data)
        #以大写搜索大写
        data=self.smallnum_to_bignum(data)
        grade_list_big=Grade.objects.filter(grade_name__contains=data)
        grade_list=grade_list_small|grade_list_big
        return grade_list

    #通过关键字得到班级集合
    def custom_get_class_list(self,class_name):
        #以小写模式查找集合
        data=self.bignum_to_smallnum(class_name)
        class_list_small=Class.objects.filter(class_name__contains=data)
        #以大写搜索大写
        data=self.smallnum_to_bignum(data)
        class_list_big=Class.objects.filter(class_name__contains=data)
        class_list=class_list_small|class_list_big
        return class_list

    #字符串中的大写改成小写
    def bignum_to_smallnum(self,data):
        mapping={'一':'1','二':'2','三':'3','四':'4','五':'5','六':'6','七':'7','八':'8','九':'9',}
        for num in mapping:
            data=data.replace(num,mapping[num])
        return data


    #字符串中的小写改成大写
    def smallnum_to_bignum(self,data):
        mapping={'1':'一','2':'二','3':'三','4':'四','5':'五','6':'六','7':'七','8':'八','9':'九'}
        for num in mapping:
            data=data.replace(num,mapping[num])
        return data

# ---------------------------------------------------------------------------- R


#注册学生
class RegStudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,help_text='输入密码')
    class_id=serializers.CharField(write_only=True,help_text='输入班级id')
    class Meta:
        model=Users
        fields=('name','mobile','password','class_id',)

    def validate(self, data):
        if not Roles.objects.filter(role='学生').first():
            Roles.objects.create(role='学生')
        if not Class.objects.filter(pk=data.get('class_id')):
            raise serializers.ValidationError('没有找到这个班级id')
        return data

    def create(self, validated_data):
        #创建用户
        name=validated_data.get('name')
        mobile=validated_data.get('mobile')
        password=validated_data.get('password')
        user=self.create_user(data={'username':mobile,'name':name,'mobile':mobile,'password':password})
        user_id=user.id
        #绑定角色
        self.create_role(user_id)
        #关联学生
        student_instance=self.create_student(data={'user':user_id})
        student_id=student_instance.id
        #绑定班级 验证
        class_id=validated_data.get('class_id')
        data={'student':student_id,'s_class':class_id}
        self.create_class(data)
        #返回用户实例
        return user

    #1.创建用户
    def create_user(self,data):
        serializer_user = UsersSerializer(data=data)
        if serializer_user.is_valid():
            serializer_user.save()
            user=serializer_user.instance
            return user
        else:
            raise Exception(serializer_user.errors)

    #2.绑定角色
    def create_role(self,user_id):
        role_obj=Roles.objects.filter(role='学生').first()
        role_id=role_obj.id
        data={'user':user_id,'role':role_id}
        serializer_usersroles=UsersRolesSerializer(data=data)
        if serializer_usersroles.is_valid():
            serializer_usersroles.save()
            return serializer_usersroles.instance
        else:
            raise Exception(serializer_usersroles.errors)

    #3.绑定学生
    def create_student(self,data):
        serializer=StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            student_instance=serializer.instance
            return student_instance
        else:
            raise Exception(serializer.errors)

    #4.绑定班级
    def create_class(self,data):

        serializer=ClassStudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.instance
        else:
            raise Exception(serializer.errors)


#注册老师
class RegTeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,help_text='输入密码')
    class_id=serializers.CharField(write_only=True,help_text='输入班级id')
    is_valied=serializers.BooleanField(write_only=True)
    # re_password=serializers.BooleanField(write_only=True)
    #学校年级班级
    school_name=serializers.SerializerMethodField()
    grade_name=serializers.SerializerMethodField()
    class_name=serializers.SerializerMethodField()

    def get_school_name(self,obj):
        school_obj=School.objects.filter(
            schoolgrade__grade__gradeclass__class_name__classteacher__teacher__user=obj).first()
        if not school_obj: return ''
        return school_obj.school_name

    def get_grade_name(self,obj):
        grade_obj=Grade.objects.filter(gradeclass__class_name__classteacher__teacher__user=obj).first()
        if not grade_obj:return ''
        return grade_obj.grade_name

    def get_class_name(self,obj):
        if not obj:return ''
        class_obj=Class.objects.filter(classteacher__teacher__user=obj).first()
        if not class_obj:return ''
        return class_obj.class_name

    class Meta:
        model=Users
        fields=('name','mobile','password','class_id','is_valied',
                'school_name','grade_name','class_name',)
        read_only_fields=('school_name','grade_name','class_name',)


    def validate(self, data):
        if not Roles.objects.filter(role='老师').first():
            Roles.objects.create(role='老师')
        if not Class.objects.filter(pk=data.get('class_id')):
            raise serializers.ValidationError('没有找到这个班级id')
        return data

    #创建老师需要执行的系列步骤
    def create(self, validated_data):
        #1.创建用户
        name=validated_data.get('name')
        mobile=validated_data.get('mobile')
        password=validated_data.get('password')
        user=self.create_user(data={'name':name,'mobile':mobile,'password':password})
        user_id=user.id
        #2.绑定角色
        self.create_role(user_id)
        #3.创建老师
        is_valied=validated_data.get('is_valied',False)
        teacher_instance=self.create_teacher(data={'user':user_id,'is_valied':is_valied})
        teacher_id=teacher_instance.id
        # 4.绑定班级  定位班级/绑定班级
        class_id=validated_data.get('class_id')
        data={'teacher':teacher_id,'class_name':class_id}
        self.create_class(data)
        #返回用户实例
        return user

    #1.创建用户
    def create_user(self,data):
        serializer_user = UsersSerializer(data=data)
        if serializer_user.is_valid():
            serializer_user.save()
            user=serializer_user.instance
            return user
        else:
            raise serializers.ValidationError(serializer_user.errors)

    #2.绑定角色
    def create_role(self,user_id):
        role_obj=Roles.objects.filter(role='老师').first()
        role_id=role_obj.id
        data={'user':user_id,'role':role_id}
        serializer_usersroles=UsersRolesSerializer(data=data)
        if serializer_usersroles.is_valid():
            serializer_usersroles.save()
            return serializer_usersroles.instance
        else:
            raise Exception(serializer_usersroles.errors)

    #3.绑定老师
    def create_teacher(self,data):
        serializer=TeacherSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            teacher_instance=serializer.instance
            return teacher_instance
        else:
            raise Exception(serializer.errors)

    #4.绑定班级
    def create_class(self,data):

        serializer=ClassTeacherSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.instance
        else:
            raise Exception(serializer.errors)


#注册一个老师
class RegOneTeacherSerializer(RegTeacherSerializer):
    code=serializers.CharField(write_only=True,help_text='请输入手机验证码')
    valied=serializers.SerializerMethodField()

    def get_valied(self,obj):
        teacher_obj=Teacher.objects.filter(user=obj).first()
        if not teacher_obj:return ''
        if teacher_obj.is_valied:
            return '有效用户'
        else:
            return '无效用户'

    class Meta:
        model=RegTeacherSerializer.Meta.model
        fields=RegTeacherSerializer.Meta.fields+('id','code','valied',)

    def validate(self, data):
        mobile=data.get('mobile')
        code=data.get('code')
        now=get_utc_now()
        if not Codes.objects.filter(mobile=mobile,code=code,type=1):
            raise serializers.ValidationError('验证码无效')
        if not Codes.objects.filter(mobile=mobile,code=code,type=1,created_at__gt=now-settings.EFFECTIVE_TIME):
            raise serializers.ValidationError('验证码已过期')
        data['is_valied']=False
        serializer=RegTeacherSerializer(data=data)
        if serializer.is_valid():
            self.reg_serializer=serializer
        else:
            raise serializers.ValidationError(serializer.errors)
        return data

    def create(self,data):
        return self.reg_serializer.save()


#资源
class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resources
        fields=('id','resource','help')


#权限
class ResourceRoleActionSerializer(serializers.ModelSerializer):
    api=serializers.CharField(source='resource.resource',read_only=True)
    api_help=serializers.CharField(source='resource.help',read_only=True)
    role_help=serializers.CharField(source='role.role',read_only=True)
    action_help=serializers.CharField(source='action.help',read_only=True)

    class Meta:
        model=ResourceRoleAction
        fields=('id','create_at','update_at','resource','role','action','api','api_help','role_help','action_help')


#角色表序列化
class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Roles
        fields=('id','role','created_at','updated_at')


# ---------------------------------------------------------------------------- S


#学生
class StudentSerializer(serializers.ModelSerializer):
    user_id=serializers.CharField(source='user.id',read_only=True)
    student_name=serializers.CharField(source='user.name',read_only=True)
    school=serializers.SerializerMethodField(read_only=True)
    grade=serializers.SerializerMethodField(read_only=True)
    class_name=serializers.SerializerMethodField(read_only=True)
    questionnaires=serializers.SerializerMethodField(read_only=True)

    def get_school(self,obj):
        schools=School.objects.filter(schoolgrade__grade__gradeclass__class_name__classstudent__student=obj)
        schools_info = []
        for s in schools:
            schools_info.append(s.school_name)
        return schools_info

    def get_grade(self,obj):
        grade=Grade.objects.filter(gradeclass__class_name__classstudent__student=obj)
        grade_info = []
        for g in grade:
            grade_info.append(g.grade_name)
        return grade_info

    def get_class_name(self,obj):
        classes=ClassStudent.objects.filter(student=obj)
        class_info=[]
        for c in classes:
            class_info.append(c.s_class.class_name)
        return class_info

    def get_questionnaires(self,obj):
        questionnaire_objs=Questionnaire.objects.filter(studentquestionnaire__student_obj=obj)
        return [questionnaire_obj.questionnaire_name for questionnaire_obj in questionnaire_objs]


    class Meta:
        model=Student
        fields=('id','user','user_id','student_name','class_name','school','grade','questionnaires',)


#学生问卷
class StudentQuestionnaireSerializer(serializers.ModelSerializer):

    def __new__(cls,*args,**kwargs):

        #制作可以选择的学生范围
        try:
            view=kwargs.get('context').get('view')
        except:
            try:
                view=kwargs.get('data').get('view')
            except:
                return super().__new__(cls, *args, **kwargs)
        user =view.request.user
        if user:
            roles=get_user_role(user)
            if '老师' in roles:
                #定位老师
                teacher_objs=Teacher.objects.filter(user=user)
                #制作学生集
                query_kwargs={'classstudent__s_class__classteacher__teacher__in':teacher_objs}
                for option in get_query(Student,kwargs=query_kwargs):
                    cls.choices.append(option)
        return super().__new__(cls,*args,**kwargs)

    student_name=serializers.CharField(source='student_obj.user.name',read_only=True)
    student_school =serializers.SerializerMethodField()
    student_grade =serializers.SerializerMethodField()
    student_class =serializers.SerializerMethodField()
    choices=[]
    student_obj=serializers.ChoiceField(choices=choices,write_only=True)
    questionnaire_name=serializers.CharField(source='questionnaire_obj.questionnaire_name',
                                             read_only=True)
    questionnaire_code =serializers.CharField(source='questionnaire_obj.questionnaire_code',
                                             read_only=True)
    questionnaire_type=serializers.CharField(source='questionnaire_obj.questionnaire_type',
                                             read_only=True)

    status_help=serializers.SerializerMethodField(read_only=True)
    status=serializers.BooleanField(read_only=True)

    def get_student_school(self,obj):
        school_obj=School.objects.filter(
            schoolgrade__grade__gradeclass__class_name__classstudent__student=obj.student_obj).first()
        return school_obj.school_name

    def get_student_grade(self, obj):
        grade_obj = Grade.objects.filter(
            gradeclass__class_name__classstudent__student=obj.student_obj).first()
        return grade_obj.grade_name

    def get_student_class(self, obj):
        class_obj = Class.objects.filter(
            classstudent__student=obj.student_obj).first()
        return class_obj.class_name


    def get_status_help(self,obj):
        if obj.status:
            return '问卷开放中[参与者还未填写]'
        else:
            return '问卷已关闭[已提交或已过期]'

    def validate_student_obj(self, attrs):
        try:
            student_obj=Student.objects.filter(pk=attrs).first()
            if not student_obj:
                raise serializers.ValidationError('不能通过学生id找到这个学生[未找到]')
            return student_obj
        except:
            raise serializers.ValidationError('不能通过学生id找到这个学生[参数格式不正确]')

    class Meta:
        model=StudentQuestionnaire
        fields=('id','create_at','student_obj','questionnaire_obj',
                'questionnaire_name','questionnaire_code','questionnaire_type',
                'status','status_help',
                'student_school','student_grade','student_class','student_name',)

#任务
class StudentQuestionnaireReadOnlySerializer(serializers.ModelSerializer):
    #姓名 手机 问卷 状态
    name=serializers.SerializerMethodField()
    mobile=serializers.SerializerMethodField()
    questionnaire=serializers.SerializerMethodField()
    status_help=serializers.SerializerMethodField()

    def get_name(self,obj):
        return obj.student_obj.user.name

    def get_mobile(self,obj):
        return obj.student_obj.user.mobile

    def get_questionnaire(self,obj):
        return obj.questionnaire_obj.questionnaire_name

    def get_status_help(self,obj):
        return '问卷进行中' if obj.status else '问卷已关闭'

    class Meta:
        model=StudentQuestionnaire
        fields=('name','mobile','questionnaire','status_help',
                'create_at','student_obj','questionnaire_obj','status',)


#学校年级
class SchoolGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model=SchoolGrade
        fields=('school','grade',)


#学校
class SchoolSerializer(serializers.ModelSerializer):
    city_id=serializers.ChoiceField(choices=get_query(City),write_only=True)
    province_city=serializers.SerializerMethodField()

    def get_province_city(self,obj):
        city_obj=City.objects.filter(cityschool__school_obj=obj).first()
        if city_obj:
            return str(city_obj)
        else:
            return 'xx省xx市(未定义)'
    class Meta:
        model=School
        fields=('id','school_name','city_id','province_city',)

    def create(self, validated_data):
        city_id=validated_data.pop('city_id')
        school_obj=super().create(validated_data)
        school_id=school_obj.id
        data={'city_obj':city_id,'school_obj':school_id}
        serializer=CitySchoolSerialzier(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise serializers.ValidationError('城市与学校的关联关系初始化失败.请手动为此学校添加到所属城市.')
        return school_obj


#校长
class SchoolMasterSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source='user_obj.name',read_only=True)
    school_name=serializers.CharField(source='school_obj.school_name',read_only=True)
    school_id=serializers.ChoiceField(choices=get_query(School),write_only=True)
    name=serializers.CharField(write_only=True)
    mobile=serializers.CharField(write_only=True)
    password=serializers.CharField(write_only=True)
    class Meta:
        model=SchoolMaster
        fields=('id','user_obj','school_obj','user_name','school_name',
                'school_id','name','mobile','password',)
        read_only_fields=('user_obj','school_obj',)

    def validate(self, data):
        if not Roles.objects.filter(role='校长').first():
            Roles.objects.create(role='校长')
        if not School.objects.filter(pk=data.get('school_id')):
            raise serializers.ValidationError('通过这个id没有找到对应学校')
        return super().validate(data)


    #创建学校需要执行的系列步骤
    def create(self, validated_data):
        #1.创建用户
        name=validated_data.get('name')
        mobile=validated_data.get('mobile')
        password=validated_data.get('password')
        user=self.create_user(data={'name':name,'mobile':mobile,'password':password})
        user_id=user.id
        #2.绑定角色
        self.create_role(user_id)
        #3.绑定学校  定位学校/绑定学校
        school_id=validated_data.get('school_id')
        data={'user_obj':user,'school_obj':School.objects.filter(pk=school_id).first()}
        return super().create(data)

    #1.创建用户
    def create_user(self,data):
        serializer_user = UsersSerializer(data=data)
        if serializer_user.is_valid():
            serializer_user.save()
            user=serializer_user.instance
            return user
        else:
            raise Exception(serializer_user.errors)

    #2.绑定角色
    def create_role(self,user_id):
        role_obj=Roles.objects.filter(role='校长').first()
        role_id=role_obj.id
        data={'user':user_id,'role':role_id}
        serializer_usersroles=UsersRolesSerializer(data=data)
        if serializer_usersroles.is_valid():
            serializer_usersroles.save()
            return serializer_usersroles.instance
        else:
            raise serializers.ValidationError(serializer_usersroles.errors)
            # raise Exception(serializer_usersroles.errors)


# ---------------------------------------------------------------------------- T


#老师
class TeacherSerializer(serializers.ModelSerializer):
    teacher_name=serializers.CharField(source='user.name',read_only=True)
    class_name=serializers.SerializerMethodField()
    school=serializers.SerializerMethodField()
    grade=serializers.SerializerMethodField()

    def get_grade(self,obj):
        grade=Grade.objects.filter(gradeclass__class_name__classteacher__teacher=obj)
        grade_info = []
        for g in grade:
            grade_info.append(g.grade_name)
        return grade_info

    def get_school(self,obj):
        schools=School.objects.filter(schoolgrade__grade__gradeclass__class_name__classteacher__teacher=obj)
        schools_info = []
        for s in schools:
            schools_info.append(s.school_name)
        return schools_info

    def get_class_name(self,obj):
        classes=ClassTeacher.objects.filter(teacher=obj)
        class_info=[]
        for c in classes:
            class_info.append(c.class_name.class_name)
        return class_info

    class Meta:
        model=Teacher
        fields=('id','user','teacher_name','school','class_name','grade','is_valied',)


#token
class TokensSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=30,help_text='输入用户名')
    password=serializers.CharField(max_length=100,help_text='输入密码')


#从电子表格注册学生同时添加任务
class TaskFromXlsxSerializer(serializers.Serializer):
    file=serializers.FileField(write_only=True)
    questionnaire_id=serializers.CharField(write_only=True,help_text='从这里输入问卷的id')

    #1.对上传的文件进行解析并验证
    def validate_file(self, file):
        path='files/{}_{}'.format(time.time(),file.name)
        with open(path,'wb') as f:
            for i in file.chunks():
               f.write(i)
        wb = openpyxl.load_workbook(path)
        try:
            sheet=wb.get_sheet_by_name('批量注册')
        except:
            raise serializers.ValidationError('在本文件中没有发现名为[批量注册]的sheet.')
        h, l = sheet.max_row, sheet.max_column
        lines=sheet['A1':'{}{}'.format(chr(ord('A')+l-1),h)]
        datas=[]
        for line in lines:
            infos=[cell.value for cell in line]
            datas.append(infos)

        field_info=datas[0]
        body_info=datas[1:]

        field_info =self.my_validate_field_info(field_info)
        bodys=self.my_validate_body_info(body_info)
        os.remove(path)
        return field_info, body_info

    def validate_questionnaire_id(self,questionnaire_id):
        class_id=self.initial_data.get('class_id')
        if not ClassQuestionnaire.objects.filter(class_obj__id=class_id,questionnaire_obj__id=questionnaire_id):
            raise_error('这个班级不存在这份问卷')
        return Questionnaire.objects.get(id=questionnaire_id)

    #验证标题
    def my_validate_field_info(self,field_info):
        try:
            if field_info[0]!='学生姓名':
                raise serializers.ValidationError('请按照任务模板格式填写[第1列标题应该为学生姓名]')
            if field_info[1] != '手机号':
                raise serializers.ValidationError('请按照任务模板格式填写[第1列标题应该为手机号]')
        except:
            raise serializers.ValidationError('请按照任务模板格式填写')
        return field_info

    #验证内容
    def my_validate_body_info(self,body_info):
        bodys=[]
        self.validated_serializers=[]
        self.error=[]
        for line in body_info:
            if (not line[0]) and (not line[1]):
                continue

            if not line[0] or not line[1]:
                raise serializers.ValidationError('请按照任务模板格式填写[第1列为学生姓名,第2列为手机号]')
            student_data = {'name': line[0], 'mobile': line[1], 'password': self.get_password(),
                            'class_id': self.get_class_id()}

            reg_serializer=RegStudentSerializer(data=student_data)

            if reg_serializer.is_valid():
                #如果学生信息不存在,加入序列化器,准备保存
                self.validated_serializers.append([reg_serializer,True])
            else:
                if ('unique' in str(reg_serializer.errors)) and ('mobile' in str(reg_serializer.errors)):
                    #如果用户原本是存在的,直接把提交的信息暂放,待处理
                    mobile=student_data.get('mobile')
                    if Student.objects.filter(user__mobile=mobile):
                        self.validated_serializers.append([student_data, False])
                    else:
                        self.error.append('试图把一个非学生角色加入到任务中:{}'.format(mobile))
                else:
                    self.error.append(reg_serializer.errors)
        return bodys

    def get_password(self):
        password=[str(random.randint(0,9)) for i in range(10)]
        password=''.join(password)
        return password

    def get_class_id(self):
        class_id=self.initial_data.get('class_id',None)
        return class_id

    def create(self,validated_data):
        #保存用户以及新建任务
        questionnaire_obj=validated_data.get('questionnaire_id')
        self.success_info={}
        task_objs=StudentQuestionnaire.objects.filter(student_obj=-1)
        for serializer in self.validated_serializers:
            if serializer[1]:
                serializer[0].save()
                user_obj =serializer[0].instance
                student_obj = Student.objects.get(user=user_obj)
            else:
                mobile=serializer[0].get('mobile')
                student_obj=Student.objects.get(user__mobile=mobile)
            task_obj=self.create_task(student_obj,questionnaire_obj)
            task_objs=task_objs|task_obj
        tasks_serializer=StudentQuestionnaireReadOnlySerializer(task_objs,many=True)
        self.success_info=tasks_serializer.data
        return StudentQuestionnaire.objects.all().first()

    def create_task(self,student_obj,questionnaire_obj):
        studentquestionnaire_obj =StudentQuestionnaire.objects.filter(student_obj=student_obj,
                                            questionnaire_obj=questionnaire_obj)
        if not studentquestionnaire_obj:
            StudentQuestionnaire.objects.create(student_obj=student_obj,
                                                   questionnaire_obj=questionnaire_obj, status=True)
        return StudentQuestionnaire.objects.filter(student_obj=student_obj,
                                            questionnaire_obj=questionnaire_obj)


#管理员从这里添加任务
class TaskFromManageXlsxSerializer(TaskFromXlsxSerializer):
    class_id=serializers.CharField(write_only=True,help_text='从这里输入班级的id')



# ---------------------------------------------------------------------------- U


#用户表序列化
class UsersSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    userrole=serializers.SerializerMethodField()

    def get_userrole(self,obj):
        usersroles_objs=UsersRoles.objects.filter(user=obj)
        return [usersroles_obj.role.role  for usersroles_obj in usersroles_objs]

    class Meta:
        model=Users
        fields=('id','name','mobile','age','sex','e_maile','created_at',
                'updated_at','password','userrole',)

    def create(self,validated_data):
        from Tools.tools import set_md5_password
        password=validated_data.get('password')
        password=set_md5_password(password)
        validated_data['password']=password
        validated_data['username']=validated_data['mobile']
        if Users.objects.filter(username=validated_data['mobile']):raise serializers.ValidationError('用户名已经存在')
        return super().create(validated_data)


#修改用户密码
class UserPasswordSerializer(serializers.ModelSerializer):
    code=serializers.CharField(write_only=Teacher,help_text='输入你收到的验证码')
    mobile=serializers.CharField(write_only=Teacher,help_text='输入你的手机号')
    password=serializers.CharField(write_only=Teacher,help_text='输入新的密码')

    class Meta:
        model=Users
        fields=('code','mobile','password',)

    def validate_password(self,data):
        if len(data)<6:
            raise serializers.ValidationError('密码太短了')
        return data

    def validate_mobile(self,data):
        if not Users.objects.filter(mobile=data):
            raise serializers.ValidationError('手机号不存在')
        return data

    def validate(self, attrs):
        code=attrs.get('code')
        mobile=attrs.get('mobile')
        code_obj=Codes.objects.filter(mobile=mobile,code=code,type=2)
        if not code_obj:
            raise serializers.ValidationError('验证码不正确')
        code_obj=code_obj.filter(created_at__gt=get_utc_now()-settings.EFFECTIVE_TIME)
        if not code_obj:
            raise serializers.ValidationError('验证码已经过期了')
        return attrs

    def create(self, validated_data):
        mobile=validated_data.get('mobile')
        password=validated_data.get('password')
        user=Users.objects.get(mobile=mobile)
        user.set_password(password)
        user.save()
        self.teacher_handler(user)
        serializer=UsersSerializer(user)
        self.success_info=serializer.data
        return user

    #如果用户是老师，还需要特殊处理,修改re_repassword状态
    def teacher_handler(self,user):
        if get_user_role(user)=='老师':
            teacher_obj=Teacher.objects.filter(user=user).first()
            if not teacher_obj:raise serializers.ValidationError('当前用户没有被正确标记为老师')
            if teacher_obj.re_repassword:return
            teacher_obj.re_repassword=True
            teacher_obj.save()


#从已经注册的用户及角色中绑定两者的关系
class UsersRolesSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source='user.name',read_only=True)
    role_name=serializers.CharField(source='role.role',read_only=True)
    class Meta:
        model=UsersRoles
        fields=('id','user','role','user_name','role_name')


#用户不存在,但是角色存在.创建用户后绑定两者的关系
class UserRolesSerializer(serializers.ModelSerializer):
    choice_role=serializers.ChoiceField(choices=get_query(Roles),write_only=True)
    password=serializers.CharField(write_only=True)
    userrole=serializers.SerializerMethodField()

    def get_userrole(self,obj):
        usersroles_objs=UsersRoles.objects.filter(user=obj)
        return [usersroles_obj.role.role  for usersroles_obj in usersroles_objs]

    class Meta:
        model=Users
        fields=('id', 'name', 'mobile', 'age', 'sex', 'e_maile', 'created_at',
            'updated_at', 'password', 'userrole','choice_role',)
        read_only_fields=('userrole',)

    def create(self, validated_data):
        role_id=validated_data.pop('choice_role')
        serializer=UsersSerializer(data=validated_data)
        if serializer.is_valid():
            user_obj=serializer.save()
            user_id=user_obj.id
        else:
            raise serializers.ValidationError(serializer.errors)
        data={'user':user_id,'role':role_id}
        serializer=UsersRolesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)
        return user_obj


# ---------------------------------------------------------------------------- V


#老师账户验证
class VailedTeacherSerializer(serializers.ModelSerializer):
    teacher_name=serializers.CharField(source='user.name',read_only=True)
    class_name=serializers.SerializerMethodField()
    school=serializers.SerializerMethodField()
    grade=serializers.SerializerMethodField()
    # is_valied=serializers.BooleanField(help_text='如果老师信息正确无误请在此处打勾后提交')
    info=serializers.SerializerMethodField()
    yes=serializers.SerializerMethodField()
    no=serializers.SerializerMethodField()
    mobile=serializers.SerializerMethodField()

    def get_mobile(self,obj):
        return obj.user.mobile

    def get_yes(self,obj):
        id=obj.id
        password=id*44-9
        www='{}/validate_teacher/{}/{}/'.format(settings.ROOT_URL,id,password)
        return www

    def get_no(self,obj):
        id=obj.id
        password=id*44-10
        www='{}/validate_teacher/{}/{}/'.format(settings.ROOT_URL,id,password)
        return www

    # send_sms=serializers.ChoiceField(choices=((True,'发送通知'),(False,'不发送通知'),),help_text='是否通知用户',write_only=True)
    # valied=serializers.ChoiceField(choices=((True,'审核通过'),(False,'审核不通过'),),help_text='是否通过审核',write_only=True)

    def get_info(self,obj):
        if obj.is_valied:
            return '此用户已通过验证'
        else:
            return '此用户暂时未通过验证'

    def get_grade(self,obj):
        grade=Grade.objects.filter(gradeclass__class_name__classteacher__teacher=obj)
        grade_info = []
        for g in grade:
            grade_info.append(g.grade_name)
        return grade_info[0] if grade_info else ''

    def get_school(self,obj):
        schools=School.objects.filter(schoolgrade__grade__gradeclass__class_name__classteacher__teacher=obj)
        schools_info = []
        for s in schools:
            schools_info.append(s.school_name)
        return schools_info[0] if schools_info else ''

    def get_class_name(self,obj):
        classes=ClassTeacher.objects.filter(teacher=obj)
        class_info=[]
        for c in classes:
            class_info.append(c.class_name.class_name)
        return class_info[0] if class_info else ''

    def update(self, instance, validated_data):
        is_valied =validated_data.get('valied',None)
        send_sms=validated_data.get('send_sms',None)
        instance.is_valied=is_valied
        instance.save()
        if is_valied:
            send_info='{},您已成功注册成为瓦力工厂教师用户,您的用户名为：{},请及时登陆{}网站,' \
                      '修改您的密码.'.format(instance.user.name,instance.user.mobile,
                                       '{}/index'.format(settings.CODE_URL))
        else:
            send_info='{},非常抱歉,您未通过瓦力工厂的网站的注册审核,本功能仅对相关校园用户开放,' \
                      '如有疑问请联系021-54712208,谢谢！'.format(instance.user.name)
        if send_sms:
            sms=SendSMS(mobile=instance.user.mobile,data=send_info)
            stauts=sms.send()
            if stauts:
                return instance
            else:
                raise serializers.ValidationError(sms.error_info)
        else:
            raise instance


    class Meta:
        model=Teacher
        fields=('teacher_name','school','grade','class_name','mobile',
                'info','yes','no','is_valied',)
        read_only_fields=('is_valied',)


# ---------------------------------------------------------------------------- W


#等待发送信息的任务
class WaitSendSerialzier(serializers.ModelSerializer):
    def __new__(cls,*args,**kwargs):
        obj=super().__new__(cls,*args,**kwargs)
        obj.my_args,obj.my_kwargs=args,kwargs
        obj.success_info = []
        return obj
    status_help=serializers.SerializerMethodField()
    content_type_help=serializers.SerializerMethodField()
    name=serializers.CharField(source='user.name',read_only=True)
    choices=(
        (1,'发送这些短信'),
        (2,'不发送,删除这些任务或记录'),
        (3,'不发送,关闭这些任务.但是保留记录.'),
        # (4,'把这些集合里已经关闭的任务重新开启[使其处于未发送状态]'),
    )
    order=serializers.ChoiceField(choices=choices,write_only=True)
    def get_content_type_help(self,obj):
        content_type=int(obj.content_type)
        return list(filter(lambda x:True if content_type==x[0] else False,obj.choices))[0][1]

    def get_status_help(self,obj):
        if obj.status:
            return '开放中,等待被发送'
        else:
            return '已关闭,短信已经被发送或者已经被关闭'

    class Meta:
        model=WaitSend
        fields=('name','content','status_help','content_type_help','remark','create_at',
                'id','user','status','content_type','order',)
        read_only_fields=('name','content','status_help','content_type_help','remark','create_at',
                'id','user','status','content_type',)

    def success_append(self,user,data):
        name=user.name
        mobile=user.mobile
        info='[{}]--[{}]--{}'.format(name,mobile,data.replace('<br>',''))
        self.success_info.append(info)

    def create(self,data):
        context=self.my_kwargs.get('context')
        view=context.get('view')
        return_obj=view.queryset.first()
        order=data.get('order')
        waitsend_objs = view.get_queryset()
        now = datetime.datetime.now()
        #发送这些短信
        if order==1:
            for waitsend in waitsend_objs:
                user=waitsend.user
                name=user.name
                mobile=user.mobile
                content=waitsend.content
                teacher_name=name
                info='{}老师,{}'.format(teacher_name,content)
                sms=SendSMS(mobile=mobile,data=info,log='青青草原')
                success_status=sms.send()

                if not success_status:
                    error_info=sms.error_info
                    error_info='<br>[在{}时间点发送时失败了.原因为{}]'.format(now,error_info)
                    self.success_append(user,error_info)
                    waitsend.remark=waitsend.remark+error_info
                    waitsend.save()
                else:
                    waitsend.status =False
                    the_success_info='<br>[在{}时间点发送成功]'.format(now)
                    self.success_append(user, the_success_info)
                    waitsend.remark = waitsend.remark +the_success_info
                    waitsend.save()

        #删除这些任务或记录
        elif order==2:
            waitsend_objs.delete()
            self.success_info.append('提示信息：删除成功')
        #关闭这些任务
        elif order==3:
            for waitsend_obj in waitsend_objs:
                user=waitsend_obj.user
                if waitsend_obj.status==True:
                    waitsend_obj.status=False
                    the_success_info = '<br>[在{}时间点手动关闭了这个任务]'.format(now)
                    self.success_append(user, the_success_info)
                    waitsend_obj.remark = waitsend_obj.remark + the_success_info
                    waitsend_obj.save()
        #重新开启这些任务
        elif order==4:
            for waitsend_obj in waitsend_objs:
                if waitsend_obj.status == False:
                    user = waitsend_obj.user
                    waitsend_obj.status=True
                    the_success_info = '<br>[在{}时间点手动开启了这个任务]'.format(now)
                    self.success_append(user, the_success_info)
                    waitsend_obj.remark = waitsend_obj.remark + the_success_info
                    waitsend_obj.save()
        else:
            raise serializers.ValidationError('不存在的命令选项')
        return return_obj


#老师向学生配发问卷时新建的任务
class WaitSendStudentSmSSerializer(serializers.ModelSerializer):
    class Meta:
        model=WaitSendStudentSmS
        fields=('id','created_at','updated_at','student_obj','questionnaire_obj','content','success_status',)

    def sms_send(self):
        #启动这条任务的发送
        #得到号码及内容
        #更新表状态
        the_task_obj=self.instance
        mobile=the_task_obj.student_obj.user.mobile
        content=the_task_obj.content
        sms=SendSMS(mobile=mobile,data=content)
        if sms.send():
            the_task_obj.success_status=True
            the_task_obj.save()


# ---------------------------------------------------------------------------- X
# ---------------------------------------------------------------------------- Y
# ---------------------------------------------------------------------------- Z














