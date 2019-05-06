from rest_framework import serializers
from .models import *
from Tools.tools import get_user_role
from django.conf import settings
import datetime,openpyxl



class TeacherMainSerializer(serializers.Serializer):
    pass


#问卷的短信通知状态
class QuestionnaireSmsStatusSerialzier(serializers.ModelSerializer):
    questionnaire_id=serializers.CharField(write_only=True)
    class Meta:
        model=Questionnaire
        fields=('id','questionnaire_name','sms_status','questionnaire_id',)
        read_only_fields=('id','questionnaire_name','sms_status',)


#通过这个序列化器生成下载文件
class TaskDownSerializer(serializers.Serializer):
    '''
    仅用于特定的接口
    '''
    #拿到问卷id*
    #对比此角色是否与这个问卷有关系*
    #通过序列化器生成文件及地址
    #通过序列化器拿到静态文件地址
    #跳转到静态文件地址
    questionnaire_id=serializers.CharField(write_only=True)

    def validate_questionnaire_id(self, questionnaire_id):
        questionnaire_obj=Questionnaire.objects.filter(pk=questionnaire_id).first()
        if not questionnaire_obj:raise serializers.ValidationError('要查看的问卷不存在')
        roles=get_user_role(self.user)
        city_head=settings.CITYHEAD
        school_master=settings.SCHOOLHEAD
        if city_head in roles:
            self.role=city_head
            city_objs=City.objects.filter(citycityhead__city_head_obj=self.user)
            self.path_info='{}市区的问卷详情'.format([city_obj.city_name for city_obj in city_objs])
            questionnaire_obj=Questionnaire.objects.filter(pk=questionnaire_obj.id,
                classquestionnaire__class_obj__gradeclass__grade__schoolgrade__school__cityschool__city_obj__in
                =city_objs).first()
            if not questionnaire_obj:raise serializers.ValidationError('问卷不属于当前用户')
        elif school_master in roles:
            self.role =  school_master
            school_objs=School.objects.filter(schoolmaster__user_obj=self.user)
            self.path_info = '{}学校的问卷详情'.format([school_obj.school_name for school_obj in school_objs])
            questionnaire_obj=Questionnaire.objects.filter(pk=questionnaire_obj.id,
                classquestionnaire__class_obj__gradeclass__grade__schoolgrade__school__in
                =school_objs).first()
            if not questionnaire_obj:raise serializers.ValidationError('问卷不属于当前用户')
        else:
            raise serializers.ValidationError('不允许的角色请求')
        return questionnaire_obj

    def create(self,validated_data):
        #得到必要的信息
            #通过问卷拿到这个城市/学校的任务列表
            #筛选错误提交中的此学校和没有被定位的问卷
        #解析这些信息：
            # 省直辖市/城市区/学校/年级/班级/问卷/问卷类型/学生姓名/手机号码/完成状态
            # 名字.学校.年级.班级.问卷编号 / 提交失败的类型 / 提交失败的详细说明 /
        #把信息生成表格，返回地址
        questionnaire_obj=validated_data.get('questionnaire_id')
        datas=self.get_needful_info(questionnaire_obj)
        parse_datas=self.parse_info(datas)

        self.path=self.datas_to_xlsx(parse_datas)
        return questionnaire_obj

    def get_needful_info(self,questionnaire_obj):
        role=self.role
        if role==settings.CITYHEAD:
            city_objs=City.objects.filter(citycityhead__city_head_obj=self.user)
            studentquestionnaire_objs=StudentQuestionnaire.objects.filter(questionnaire_obj=questionnaire_obj,
                questionnaire_obj__classquestionnaire__class_obj__gradeclass__grade__schoolgrade__school__cityschool__city_obj__in
                =city_objs)
        elif role==settings.SCHOOLHEAD:
            school_objs=School.objects.filter(schoolmaster__user_obj=self.user)
            studentquestionnaire_objs=StudentQuestionnaire.objects.filter(questionnaire_obj=questionnaire_obj,
                questionnaire_obj__classquestionnaire__class_obj__gradeclass__grade__schoolgrade__school__in
                =school_objs)
        else:
            raise serializers.ValidationError('未知错误')
        error_commit_objs=ErrorCommit.objects.filter(create_at__gt=questionnaire_obj.created_at)
        datas=[studentquestionnaire_objs.order_by('status'),error_commit_objs]
        return datas

    def parse_info(self,datas):
        studentquestionnaire_objs, error_commit_objs=datas
        studentquestionnaire_datas=self.parse_info_studentquestionnaire_objs(studentquestionnaire_objs)
        error_commit_datas=self.parse_info_error_commit_objs(error_commit_objs)
        parse_datas=[studentquestionnaire_datas,error_commit_datas]
        return parse_datas

    def parse_info_studentquestionnaire_objs(self,studentquestionnaire_objs):
        # 省直辖市/城市区/学校/年级/班级/问卷/问卷类型/学生姓名/手机号码/完成状态
        lines=[]
        for studentquestionnaire_obj in studentquestionnaire_objs:
            questionnaire_obj=studentquestionnaire_obj.questionnaire_obj
            questionnaire_name = questionnaire_obj.questionnaire_name
            questionnaire_type = questionnaire_obj.questionnaire_type.type_name
            questionnaire_url =questionnaire_obj.questionnaire_url
            student_obj=studentquestionnaire_obj.student_obj
            student_name = student_obj.user.name
            student_mobile = student_obj.user.mobile
            finish_status = '没有完成' if studentquestionnaire_obj.status else '已经完成'
            class_obj = Class.objects.filter(classstudent__student=student_obj).first()
            class_name = class_obj.class_name if class_obj else '查询失败'
            grade_obj=Grade.objects.filter(gradeclass__class_name=class_obj).first()
            grade = grade_obj.grade_name if grade_obj else '查询失败'
            school_obj=School.objects.filter(schoolgrade__grade=grade_obj).first()
            school = school_obj.school_name if school_obj else '查询失败'
            city_obj=City.objects.filter(cityschool__school_obj=school_obj).first()
            city = city_obj.city_name if city_obj else '查询失败'
            province_obj=Province.objects.filter(city=city_obj).first()
            province=province_obj.province_name if province_obj else '查询失败'
            #questionnaire_name问卷名,questionnaire_type问卷类型,questionnaire_url问卷地址,student_name学生姓名,
            # student_mobile学生电话,finish_status完成标志,class_name班级,grade年级,school学校,city城市,province省
            line=[questionnaire_name,questionnaire_type,questionnaire_url,student_name,student_mobile,
                  finish_status,class_name,grade,school,city,province]
            lines.append(line)
        return lines

    def parse_info_error_commit_objs(self,error_commit_objs):
        # 名字.学校.年级.班级.问卷编号 / 提交失败的类型 / 提交失败的详细说明 /
        lines=[]
        for error_commit_obj in error_commit_objs:
            created_at=error_commit_obj.create_at.strftime('%Y年%m月%d日%H时%M分%S秒')
            name=error_commit_obj.original_name
            school=error_commit_obj.original_school
            grade=error_commit_obj.original_grade
            class_name=error_commit_obj.original_class
            questionnaire_code=error_commit_obj.original_code
            error_help=error_commit_obj.error_help
            line=[created_at,name,school,grade,class_name,questionnaire_code,error_help]
            lines.append(line)
        return lines

    def datas_to_xlsx(self,parse_datas):
        studentquestionnaire_datas, error_commit_datas=parse_datas[0], parse_datas[1]
        wb = openpyxl.load_workbook("static/data_to_xlsx.xlsx")
        sheet=wb.get_sheet_by_name('newsheet')
        title=['问卷名称','问卷类型','问卷地址','学生姓名','手机号','完成状态','班级','年级','学校','市区','省 / 直辖市']
        self.line_to_xlsx(title, sheet, 1)
        row=1
        for index,data in enumerate(studentquestionnaire_datas):
            row=index+2
            self.line_to_xlsx(data,sheet,row)
        row=row+5
        self.line_to_xlsx([ '..............' for i in range(20)], sheet, row)
        row = row + 1
        title2=['提交日期','原始信息：名字','原始信息：学校','原始信息：年级','原始信息：班级','原始信息：问卷编号','错误报告']
        self.line_to_xlsx(title2, sheet, row)
        for index,data in enumerate(error_commit_datas):
            row=row+1
            self.line_to_xlsx(data,sheet,row)
        path='static/head_fils/{}.xlsx'.format(self.path_info)
        wb.save(path)
        path='{}/{}'.format(settings.ROOT_URL,path)
        return path

    # "http://172.16.10.132:8000/static/head_fils/['海淀小学']学校的问卷详情.xlsx"
    # }
    def line_to_xlsx(self,datas,sheet,row):
        for index,data in enumerate(datas):
            sheet_index='{}{}'.format(chr(index+ord('A')),row)
            sheet[sheet_index]=data
        return sheet


















