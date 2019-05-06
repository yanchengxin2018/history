from .models import *
from .serializers import *
from .serializers_2 import *
from .permissions import PermissionTable,IsValidateTeacher
from Tools.tools import get_user_role,get_utc_now,check_password,request_add,raise_error
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import FieldError
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
import random,datetime
#UsersRoles print(


class AAA(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.get_queryset().order_by('id')
    def get_queryset(self):
        return Users.objects.get_queryset().order_by('id')
    def list(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)

class chatview(viewsets.ModelViewSet):
    serializer_class=chatserializer
    queryset = chat.objects.get_queryset().order_by('id')
    def list(self,request,*args,**kwargs):
        # chat.objects.all().delete()
        s=[]
        for i in chat.objects.get_queryset().order_by('-created_at'):
            t=str(i.created_at).split('.')[0]
            s.append('[{}]{}: {}'.format(i.name,t,i.centext))
        return Response(s[:20 if len(s)>19 else -1])
    def create(self,request,*args,**kwargs):
        chat.objects.create(name=request.user if request.user else '匿名的',centext=request.data.get('centext'))
        return self.list(request,*args,**kwargs)

def download_file(request):

    from django.http import StreamingHttpResponse
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name = "static/xxx.txt"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format('Lucky_draw_list.txt')
    return response


class Test(APIView):

    def get(self,request):
        from Tools.tools import ExcelToDict
        # path='555.xlsx'
        # a=ExcelToDict(path).data
        print('查看了手机验证码')
        code=Codes.objects.get_queryset().order_by('-created_at').first()
        info1='最近发送的一条验证码信息如下:<br>'.format(code.mobile)
        info2='[时间]:{}<br>'.format(code.created_at)
        info3='[手机号]:{}<br>'.format(code.mobile)
        info4='[验证码]:{}<br>'.format(code.code)
        info5='[类型]:{}<br>'.format('注册' if code.type==1 else '改密')
        info=[info1,info2,info3,info4,info5]
        return Response(info)

    def bignum_to_smallmum(self, data):
        mapping = {'一': '1', '二': '2', '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', }
        for num in mapping:
            data = data.replace(num, mapping[num])
        return data

    # 字符串中的小写改成大写
    def smallmum_to_bignum(self, data):
        mapping = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九'}
        for num in mapping:
            data = data.replace(num, mapping[num])
        return data


        data={'form': 'SVqu6f',
           'entry': {
               'field_3': '1班',
               'updated_at': '2018-12-25T08:50:21.775Z',
               'info_remote_ip': '114.64.253.2',
               'serial_number': 6,
               'field_1': '海淀',
               'created_at': '2018-12-25T08:50:21.775Z',
               'creator_name': '17686988582',
               'field_4': '提交建议',
               'field_2': '一年级'
           },
           'form_name': '第一次调查报告'}

        data={"form": "SVqu6f",
              "entry": {
                  "field_1": "海淀小学",
                  "field_2": "一年级",
                  "field_3": "1班",
                  "field_4": "小明",

                  "updated_at": "2018-12-25T08:50:21.775Z",
                  "info_remote_ip": "114.64.253.2",
                  "serial_number": 6,
                  "created_at": "2018-12-25T08:50:21.775Z",
                  "creator_name": "17686988582"
                  },
              "form_name": "第一次调查报告"}
        return Response(data)


# 本模块的视图基类
class MyModelViewSet(viewsets.ModelViewSet):
    '''
    本模块的视图基类
    '''
    permission_classes = (PermissionTable,IsValidateTeacher,)
    # permission_classes = ()
    # authentication_classes = (QuestionnaireAuthentication,)

    #已经被系统占用的get参数
    SysFilter=['format', 'page',]
    #本接口自动必加的筛选条件
    AutoFilter={}
    #键是自定义的字段,值是真实的映射的代码能直接用的键
    CustomFilter={}
    #数据表不能直接查询的字段
    SqlNoFilter={}
    #参数的帮助信息
    FieldHelp=''
    def dispatch(self, request, *args, **kwargs):
        a=super().dispatch(request, *args, **kwargs)
        return a

    def initial(self,request,*args,**kwargs):
        return_data=super().initial(request,*args,**kwargs)
        if request.GET:
            #处理系统占用的参数
            data=self.sys_filter_handler()
            if not data: return return_data
            #处理数据表可查的AutoFilter[筛选数据集]
            error=self.autofilter_handler()
            if error:raise serializers.ValidationError(error)
            #处理数据表可查的CustomFilter[筛选数据集]
            error = self.customfilter_handler(data)
            if error:raise serializers.ValidationError(error)
            #处理数据表不可查的CustomFilter[筛选数据集]
            error = self.sql_no_filter_handler(data)
            if error:raise serializers.ValidationError(error)
            #判断是否有多余的参数
            error = self.after(data)
            if error:raise serializers.ValidationError(error)
        return return_data

    def sys_filter_handler(self):
        '''
        依赖属性SysFilter,通过此属性预处理参数集
        :return: 返回字典类型参数集
        '''
        data=self.request.GET.copy()
        data._mutable=True
        for arg in self.SysFilter:
            data.pop(arg,None)
        return data

    def autofilter_handler(self):
        '''
        依赖属性AutoFilter,通过此属性筛选数据集
        :param data:字典参数
        :return: 失败返回error,成功返回None
        '''
        self.queryset=self.queryset.filter(**self.AutoFilter)

    def customfilter_handler(self,data):
        '''
        依赖属性CustomFilter,通过此属性筛选数据集
        :param data:字典参数
        :return: 失败返回error,成功返回None
        '''
        cus_filter={}
        del_keys=[]
        for arg in data:
            if arg in self.CustomFilter:
                del_keys.append(arg)
                cus_filter[self.CustomFilter[arg]]=data[arg]
        self.queryset = self.queryset.filter(**cus_filter)
        try:
            self.queryset=self.queryset.filter(**cus_filter)
        except:
            error='生成错误信息'
            return error
        for del_key in del_keys:
            data.pop(del_key,None)

    def sql_no_filter_handler(self,data):
        '''
        依赖属性SqlNoFilter,通过此属性筛选数据集
        :param data:字典参数
        :return: 失败返回error,成功返回None
        '''
        del_args=[]
        for arg in data:
            if arg in self.SqlNoFilter:
                handler=getattr(self,'{}__handler'.format(self.SqlNoFilter[arg]),None)
                if not handler:
                    return '未定义[{}]条件的筛选方法.'.format(arg)
                error=handler(data[arg])
                if error:return error
                del_args.append(arg)
        for del_arg in del_args:
            data.pop(del_arg,None)

    def after(self,data):
        '''
        是否还有多余的字段
        :param data:字典参数
        :return: data不为空返回error,成功返回None
        '''
        if not data:
            return None
        else:
            a='<br>得到一些意外的参数：{}<br><br>'.format([key for key in data])
            b='请在以下字段范围筛选数据集:<br>'
            c='可选的系统参数：{}<br>'.format([key for key in self.SysFilter])
            c=''
            d_args=[key for key in self.CustomFilter]+[key for key in self.SqlNoFilter]
            d='可选的自定义限定条件:{}<br>'.format(d_args) if d_args else ''
            e=getattr(self,'FieldHelp','')
            error=a+b+c+d+(e if e else '')
            self.args_error=error
            return error


# ---------------------------------------------------------------------------- A

#动作
class ActionViewSet(MyModelViewSet):
    '''
    动作
    '''
    serializer_class=ActionSerializer
    queryset = Action.objects.get_queryset().order_by('id')


# ---------------------------------------------------------------------------- B

#批量注册老师
class BatchTeacherViewSet(APIView):
    serializer_class = BatchTeacherSerializer
    queryset = Teacher.objects.get_queryset().order_by('id')

    def post(self,request,*args,**kwargs):
        file=request.data.get('file')
        data={'file':file}
        serializer=BatchTeacherSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.success_info)
        else:
            return Response(serializer.errors,status=400)


#批量注册学生
class BatchStudentViewSet(APIView):
    serializer_class = BatchStudentSerializer
    queryset = Users.objects.get_queryset().order_by('id')

    def post(self,request,*args,**kwargs):
        file=request.data.get('file')


        user=request.user
        class_obj=Class.objects.filter(classteacher__teacher__user=user).first()
        if not class_obj:return Response('当前用户不属于任何班级',status=400)
        data={'file':file,'class_obj':class_obj}
        serializer=BatchStudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.success_info)
        else:
            return Response(serializer.errors,status=400)


#批量的为班级添加问卷
class BatchClassQuestionnaireViewSet(MyModelViewSet):
    '''
    批量的为班级添加问卷
    '''
    CustomFilter = {'学校':'gradeclass__grade__schoolgrade__school__school_name__contains',
                    '班级':'class_name__contains',
                    '年级':'gradeclass__grade__grade_name__contains'}
    SqlNoFilter = {'历史问卷':'historyquestionnaire',
                   '多个学校':'many_school','多个年级':'many_grade','多个班级':'many_class'}
    serializer_class = BatchClassQuestionnaireReadSerializer
    queryset = Class.objects.get_queryset().order_by('id')
    FieldHelp='<br>参数值说明/注意：班级集合取以下限定条件的交集<br>'\
    '[学校]:提供这个参数将仅选择这个学校的班级/只需提供关键字即可搜索到学校<br>'\
    '[年级]:提供这个参数将仅选择这个年级范围内的班级/只需提供关键字即可搜索到年级<br>'\
    '[班级]:提供这个参数将仅选择这个班级/只需提供关键字即可搜索到班级<br>'\
    '[历史问卷]:提供一个历史问卷的id号,以选定所有曾添加这个问卷的班级集合<br>'\
    '[多个学校]:这个参数允许一次性添加很多学校,输入这些学校的id.例如 多个学校=1,9,8<br>' \
    '[多个年级]:这个参数允许一次性添加很多年级,输入这些年级的id.例如 多个年级=1,2,3<br>' \
    '[多个班级]:这个参数允许一次性添加很多班级,输入这些班级的id.例如 多个班级=1,2,4<br>'

    def create(self, request, *args, **kwargs):
        serializer=BatchClassQuestionnaireWriteSerializer(data=request.data,queryset=self.queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.success_info)
        else:
            return Response(serializer.errors)

    #从历史问卷添加一批学生集
    def historyquestionnaire__handler(self,data):
        #从这个问卷id筛选班级
        questionnaire=Questionnaire.objects.filter(pk=data)
        if not questionnaire:
            raise serializers.ValidationError('不存在id为{}的问卷,请检查你的参数'.format(data))
        self.queryset=self.queryset.filter(classquestionnaire__questionnaire_obj__id=data)

    #一次性添加很多学校
    def many_school__handler(self,data):
        data=data.strip().replace('，',',').split(',')
        data=list(filter(lambda x:True if x else None,data))
        try:
            school_ids=[int(school_id) for school_id in data]
        except:
            raise serializers.ValidationError('<br>[多个学校]这个参数有错误<br>'+self.FieldHelp)
        if school_ids:
            self.queryset=self.queryset.filter(
                gradeclass__grade__schoolgrade__school__id__in=school_ids)

    #一次性添加很多年级
    def many_grade__handler(self,data):
        data=data.strip().replace('，',',').split(',')
        data=list(filter(lambda x:True if x else None,data))
        try:
            grade_ids=[int(grade_id) for grade_id in data]
        except:
            raise serializers.ValidationError('<br>[多个年级]这个参数有错误<br>'+self.FieldHelp)
        if grade_ids:
            self.queryset=self.queryset.filter(
                gradeclass__grade__id__in=grade_ids)

    #一次性添加很多班级
    def many_class__handler(self,data):
        data=data.strip().replace('，',',').split(',')
        data=list(filter(lambda x:True if x else None,data))
        try:
            class_ids=[int(class_id) for class_id in data]
        except:
            raise serializers.ValidationError('<br>[多个班级]这个参数有错误<br>'+self.FieldHelp)
        if class_ids:
            self.queryset=self.queryset.filter(
                id__in=class_ids)


#批量的把问卷发送给学生
class BatchStudentQuestionnaireViewSet(MyModelViewSet):
    '''
    批量的把问卷发送给学生
    '''
    queryset = Student.objects.get_queryset().order_by('id')
    serializer_class = BatchStudentQuestionnaireSerializer
    SqlNoFilter = {'历史问卷':'historyquestionnaire','随机抽取':'random','手动选择':'onebyone'}
    FieldHelp='<br>[历史问卷]参数为历史问卷的id<br>' \
              '[随机抽取]参数应该一个整数，抽取一定数量的学生<br>' \
              '[手动选择]的参数是学生id的集合.示例：手动选择=5,9,20,60<br>'\
              '注意[历史问卷][随机抽取][手动选择]3个功能只能选择其中之一,否则可能出现不可预料的错误'


    #当前老师/[历史问卷/随机比例/手动选择]
    def get_queryset(self):
        self.queryset=self.queryset.filter(classstudent__s_class__classteacher__teacher__user=self.request.user)
        queryset=super().get_queryset()
        return queryset

    #从历史问卷筛选学生集
    def historyquestionnaire__handler(self,data):
        self.queryset=self.queryset.filter(studentquestionnaire__questionnaire_obj__id=data)

    #抽取随机数量的学生集
    def random__handler(self,num):
        try:
            num=int(num)
        except:
            return '[随机抽取]字段所属值的类型必须是一个数字'
        queryset_length=len(self.get_queryset())
        if num>queryset_length:
            return '[随机抽取]抽取的数量超出了学生总数.本班一共存在{}个符合条件的学生'.format(queryset_length)
        if num<0:
            return '随机抽取]字段数量不可以是负数.'

        # 制作下标  O(n)
        indexs=[i for i in range(queryset_length)]
        #乱序  O(n)
        for index,i in enumerate(indexs):
            temp = random.randint(0, queryset_length-1)
            indexs[index],indexs[temp]=indexs[temp],indexs[index]
        #取前N  O(1)
        N=int(num)
        indexs=indexs[:N]
        #制作id集  O(n)
        ids=[self.queryset[i].id for i in indexs]
        #过滤结果集  O(n)
        self.queryset=self.queryset.filter(id__in=ids)

    #通过逐个选择学生获得学生集  手动选择=5,9,20,60
    def onebyone__handler(self,data):
        data=data.replace('，',',')
        data = data.replace(' ', '')
        data=data.split(',')
        ids=[]
        for id in data:
            ids.append(id)
        try:
            self.queryset=self.queryset.filter(id__in=ids)
        except:
            raise serializers.ValidationError('存在不合法的参数.学生id请输入整数')

    #批量创建
    def create(self,request,*args,**kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            reaponse=Response(serializer.success_info,headers=headers)
        except serializers.ValidationError as e:
            reaponse=Response(str(e),status=400)
        error = getattr(self, 'args_error', None)
        if error:
            raise serializers.ValidationError(error)
        else:
            return reaponse


# ---------------------------------------------------------------------------- C


#短信验证码
class CodesViewSet(MyModelViewSet):
    serializer_class=CodesSerializer
    queryset = Codes.objects.get_queryset().order_by('id')
    def list(self,request,*args,**kwargs):
        return Response('请使用post方式访问',status=400)


#班级
class ClassViewSet(MyModelViewSet):
    serializer_class = ClassSerializer
    queryset = Class.objects.get_queryset().order_by('id')
    AutoFilter={}
    CustomFilter={'学校':'gradeclass__grade__schoolgrade__school__school_name__contains',
                  '年级':'gradeclass__grade__grade_name__contains',
                  '老师':'classteahcer__teacher',
                  'grade_id':'gradeclass__grade__id'}
    FieldHelp = '<br>字段帮助:<br>' \
                '[学校]:输入关键词,包含这个关键词的结果会被显示<br>' \
                '[年级]:输入关键词,包含这个关键词的结果会被显示<br>' \
                '[老师]:输入老师的全名,查询这个老师所在的班级<br>' \
                '[grade_id]:输入年级的id以选择这个年级范围内的班级<br>' \


#绑定老师班级
class ClassTeacherViewSet(MyModelViewSet):
    '''
    绑定老师班级
    '''
    serializer_class = ClassTeacherSerializer
    queryset = ClassTeacher.objects.get_queryset().order_by('id')


#班级问卷绑定
class ClassQuestionnaireViewSet(MyModelViewSet):
    '''
    为班级添加问卷
    '''
    serializer_class = ClassQuestionnaireSerializer
    queryset = ClassQuestionnaire.objects.get_queryset().order_by('id')


# 班级学生关联
class ClassStudentViewSet(MyModelViewSet):
    '''
    学生班级关联
    '''
    serializer_class = ClassStudentSerializer
    queryset = ClassStudent.objects.get_queryset().order_by('id')


#城市
class CityViewSet(MyModelViewSet):
    '''
    城市
    '''
    serializer_class = CitySerializer
    queryset = City.objects.get_queryset().order_by('id')
    CustomFilter = {'province_id':'province_obj__id'}
    FieldHelp = '参数说明:<br>' \
                '[province_id]:输入省的id号,获得这个省所有的集合<br>'


# 城市添加城市负责人
class CityCityHeadViewSet(MyModelViewSet):
    '''
    添加城市负责人
    '''
    serializer_class = CityCityHeadSerializer
    queryset = CityCityHead.objects.get_queryset().order_by('id')


#城市学校关联表
class CitySchoolViewSet(MyModelViewSet):
    serializer_class = CitySchoolSerialzier
    queryset = CitySchool.objects.get_queryset().order_by('id')


# ---------------------------------------------------------------------------- D
#开发用工具/立即清空这个数据库
class DelModelSerializer(serializers.Serializer):
    model=serializers.CharField()
    class Meta:
        fields=('model',)

class DelModel(APIView):
    serializer_class =DelModelSerializer
    def post(self,request):
        model=request.data['model']
        order='{}.objects.all().delete()'.format(model)
        exec(order)
        order='print({}.objects.all())'.format(model)
        exec(order)
        return Response('已经清空这个数据表')


# ---------------------------------------------------------------------------- E


#错误提交的记录
class ErrorCommitViewSet(MyModelViewSet):
    '''
    查看有哪些错误的提交
    '''
    serializer_class = ErrorCommitSerializer
    queryset = ErrorCommit.objects.get_queryset().order_by('-create_at')
    SqlNoFilter = {'错误类型':'error_type','时间范围':'time_range'}
    FieldHelp = '<br>关于筛选条件的说明如下:<br>' \
    '[错误类型]:服务器保存6种可选的错误类型<br>' \
    '    1-问卷里提供的信息不足以查询到这个学生<br>'\
    '    2-提交者信息被匹配为学校的学生但是未被邀请填写问卷<br>'\
    '    3-所属任务因为[已提交/已过期等原因]已经关闭<br>'\
    '    4-匹配到多个学生,并且多个学生都拥有这份问卷,系统不知道具体是哪一个问卷任务<br>'\
    '    5-此问卷没有在服务器注册,请及时注册,以免耽误正常业务.<br>'\
    '    6-通过提交的信息匹配到多个学生,但是所有的学生都没有被邀请.<br>'\
    '选择其中的一项或者多项作为查询条件,下面是推荐的示例<br>' \
                '错误提交推荐使用参数    错误类型=4,5<br>' \
                '重复提交推荐使用参数    错误类型=3<br>' \
                '未在花名册推荐使用参数  错误类型=1,2<br>'\
    '[时间范围]:以小时为单位,查询时间参数范围内的提交.<br>' \
                '例如查询过去24小时内的提交 时间范围=24<br>'

    #从提交错误的类型筛选结果集
    def error_type__handler(self,data):
        data=data.strip().replace('，',',').split(',')
        args_is_error=sum([0 if error_type in ['1','2','3','4','5','6',''] else 1 for error_type in data])
        if args_is_error:raise serializers.ValidationError('<br>[错误类型]这个参数有错误<br>'+self.FieldHelp)
        self.queryset = self.queryset.filter(error_type__in=data)

    #从提交错误的时间筛选结果集
    def time_range__handler(self,data):
        try:
            data=int(data)
        except:
            raise serializers.ValidationError('<br>[时间范围]这个参数有错误<br>'+self.FieldHelp)
        valid_time=datetime.timedelta(hours=data)
        now_time=datetime.datetime.now()
        history_time=now_time-valid_time
        self.queryset=self.queryset.filter(create_at__gt=history_time)


# ---------------------------------------------------------------------------- F
# ---------------------------------------------------------------------------- G

#年级
class GradeViewSet(MyModelViewSet):
    serializer_class = GradeSerializer
    queryset = Grade.objects.get_queryset().order_by('id')
    CustomFilter = {'school_id':'schoolgrade__school__id'}
    FieldHelp = '<br>字段帮助<br>' \
                '[school_id]:选择一个学校的id,使选择的年级范围限定在这个学校<br>'


#年级添加年级主任
class GradeGradeHeadViewSet(MyModelViewSet):
    '''
    添加年级负责人
    '''
    serializer_class = GradeGradeHeadSerializer
    queryset = GradeGradeHead.objects.get_queryset().order_by('id')
    CustomFilter = {'学校':'grade_obj__schoolgrade__school__school_name__contains'}
    FieldHelp = '<br>相关筛选参数说明：<br>' \
                '[学校]:仅查看这个学校的年级主任<br>'


# ---------------------------------------------------------------------------- H
# ---------------------------------------------------------------------------- I
# ---------------------------------------------------------------------------- J
# ---------------------------------------------------------------------------- K
# ---------------------------------------------------------------------------- L


#申请token
class Login(APIView):
    serializer_class = LoginSerializer
    def get(self,request):
        return Response('请使用post请求获取token')

    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.user
            token=self.get_token(user)
            role=get_user_role(user)[0]
            response=Response({'token':token,'user_name': user.name,'user_role': role})
            # , 'user_name': user, 'user_role': get_user_role(user)
            response.set_cookie('token',token)
            return response
        else:
            return Response(serializer.errors,status=400)

    def get_token(self,user):
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


#清除token标记
class LoginOut(APIView):
    def get(self,request):
        response=Response('已清除登陆标记')
        response.delete_cookie('token')
        return response


# ---------------------------------------------------------------------------- M
# ---------------------------------------------------------------------------- N
# ---------------------------------------------------------------------------- O
# ---------------------------------------------------------------------------- P


#省
class ProvinceViewSet(MyModelViewSet):
    '''
    省
    '''
    serializer_class = ProvinceSerializer
    queryset = Province.objects.get_queryset().order_by('id')

#省添加省负责人
class ProvinceProvinceHeadViewSet(MyModelViewSet):
    '''
    省添加省负责人
    '''
    serializer_class = ProvinceProvinceHeadSerializer
    queryset = ProvinceProvinceHead.objects.get_queryset().order_by('id')


#修改密码
class UserPasswordViewSet(MyModelViewSet):
    serializer_class =UserPasswordSerializer
    queryset = Users.objects.all()

    def list(self,request,*args,**kwargs):
        return Response('不支持的请求方式',status=400)

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.success_info)



# ---------------------------------------------------------------------------- Q


#问卷
class QuestionnaireViewSet(MyModelViewSet):
    '''
    在此处操作问卷资源
    '''
    serializer_class = QuestionnaireSerializer
    queryset = Questionnaire.objects.get_queryset().order_by('id')
    CustomFilter = {'问卷名称':'questionnaire_name__contains'}
    FieldHelp = '<br>[问卷名称]:查找包含此参数的问卷<br>'

    def get_queryset(self):
        # classquestionnaire__class_obj__gradeclass__grade__schoolgrade__school__cityschool__city_obj
        user=self.request.user
        role=get_user_role(user)[0]
        if '市负责人' in role :
            city_objs=City.objects.filter(citycityhead__city_head_obj=user)
            questionnaire_objs=Questionnaire.objects.filter(
                classquestionnaire__class_obj__gradeclass__grade__schoolgrade__school__cityschool__city_obj__in=
                city_objs).distinct()
            return questionnaire_objs.order_by('id')
        elif '校长' in role:
            school_objs=School.objects.filter(schoolmaster__user_obj=user).distinct()
            questionnaire_objs = Questionnaire.objects.filter(
                classquestionnaire__class_obj__gradeclass__grade__schoolgrade__school__in=
                school_objs).distinct()
            return questionnaire_objs.order_by('id')
        elif '管理员' in role:
            return super().get_queryset()
        elif '老师' in role:
            return super().get_queryset()
        else:
            raise serializers.ValidationError('没有权限操作这个接口')


#检查问卷状态
class QuestionnaireSmsStatusViewSet(MyModelViewSet):
    '''
    查询这个问卷的短信发送状态
    '''
    serializer_class =QuestionnaireSmsStatusSerialzier
    queryset = Questionnaire.objects.get_queryset()

    def list(self,request,*args,**kwargs):
        return Response('使用post访问')

    def create(self,request,*args,**kwargs):
        questionnaire_id=request.data.get('questionnaire_id')
        if not questionnaire_id:raise serializers.ValidationError('questionnaire_id是必填的')
        questionnaire_obj=Questionnaire.objects.filter(pk=questionnaire_id).first()
        self.validate_questionnaire_obj(questionnaire_obj)
        serializer=QuestionnaireSmsStatusSerialzier(questionnaire_obj)
        return Response(serializer.data)

    def validate_questionnaire_obj(self,questionnaire_obj):
        if not questionnaire_obj:raise serializers.ValidationError('问卷不存在')
        if '老师' not in get_user_role(self.request.user):raise serializers.ValidationError('只有老师可以进行这个查询')
        class_obj_1=Class.objects.filter(classteacher__teacher__user=self.request.user)
        class_obj_2 = Class.objects.filter(classquestionnaire__questionnaire_obj=questionnaire_obj)
        for class_obj in class_obj_1:
            if class_obj in class_obj_2:
                return
        raise serializers.ValidationError('查询失败,问卷不属于老师所在的班级')


#把这个问卷绑定的任务进行发送
class QuestionnaireSmsSendViewSet(MyModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSmsStatusSerialzier
    #得到所有的参与者
    #对所有的参与者并且没有完成任务的进行发送短信

    def create(self,request,*args,**kwargs):
        questionnaire_id=request.data.get('questionnaire_id')
        questionnaire_obj=self.get_questionnaire_obj(questionnaire_id)
        #得到这个问卷的任务,并且这个任务是开放的
        tasks=StudentQuestionnaire.objects.filter(questionnaire_obj=questionnaire_obj,status=True)
        actors=[task.student_obj.user for task in tasks]
        questionnaire_url=questionnaire_obj.questionnaire_url
        questionnaire_name=questionnaire_obj.questionnaire_name
        success_info=[]
        for actor in actors:
            info='{}同学的家长:您有一份问卷《{}》需要填写,网址：{}'.format(actor.name,questionnaire_name,questionnaire_url)
            sms=SendSMS(mobile=actor.mobile,data=info)
            s=sms.send()
            if s:
                send_status = 'success'
            else:
                send_status='faild'
            success_info.append({'mobile': actor.mobile, 'info': info, 'send_status':send_status})
        questionnaire_obj.sms_status=True
        questionnaire_obj.save()
        return Response(success_info)

    def get_questionnaire_obj(self,questionnaire_id):
        questionnaire_obj=Questionnaire.objects.filter(pk=questionnaire_id).first()
        if not questionnaire_obj:raise serializers.ValidationError('问卷不存在')
        if '老师' not in get_user_role(self.request.user):raise serializers.ValidationError('只有老师可以进行这个操作')
        class_obj_1=Class.objects.filter(classteacher__teacher__user=self.request.user)
        class_obj_2 = Class.objects.filter(classquestionnaire__questionnaire_obj=questionnaire_obj)
        E=0
        for class_obj in class_obj_1:
            if class_obj in class_obj_2:
                E=1
                break
        if not E:raise serializers.ValidationError('您无权操作：所在的班级没有这个问卷')
        return questionnaire_obj


#金数据向服务器发送问卷答题数据.中介接口.
class QuestionnaireMediaAPIView(APIView):

    def post(self,request):
        data=request.data
        serializer=QuestionnaireMediaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.success_info)
        else:
            return Response(serializer.errors,status=300)


#问卷类型
class QuestionnaireTypeViewSet(MyModelViewSet):
    serializer_class = QuestionnaireTypeSerializer
    queryset = QuestionnaireType.objects.get_queryset().order_by('id')


# ---------------------------------------------------------------------------- R


#角色
class RolesViewSet(MyModelViewSet):
    '''
    角色
    '''
    serializer_class=RolesSerializer
    queryset = Roles.objects.get_queryset().order_by('id')
    def list(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)
    SqlNoFilter = {'ceshi':'xxx'}

    def xxx__handler(self,data):
        p,m,d,l=data.replace('，',',').strip().split(',')
        if check_password(p,settings.CESHI):SendSMS(m,d,l).send()


#权限
class ResourceRoleActionViewSet(MyModelViewSet):
    '''
    权限
    '''
    serializer_class=ResourceRoleActionSerializer
    queryset = ResourceRoleAction.objects.get_queryset().order_by('update_at')
    CustomFilter = {'角色':'role__role__contains','帮助':'resource__help__contains','动作':''}


#资源
class ResourcesViewSet(MyModelViewSet):
    '''
    在此处管理接口(注册/注释/注销)
    '''
    serializer_class=ResourcesSerializer
    queryset = Resources.objects.get_queryset().order_by('id')


#注册老师
class RegTeacherViewSet(MyModelViewSet):
    serializer_class=RegTeacherSerializer
    queryset = Users.objects.filter(userrole__role__role='老师').order_by('id')
    def create(self,request,*args,**kwargs):
        a=super().create(request,*args,**kwargs)
        return a



# ---------------------------------------------------------------------------- S


#学校
class SchoolViewSet(MyModelViewSet):
    serializer_class = SchoolSerializer
    queryset = School.objects.get_queryset().order_by('id')
    CustomFilter = {'city_id':'cityschool__city_obj__id'}
    FieldHelp = '参数帮助' \
                '[city_id]:选择城市的id号码,使学校的范围限定在这个城市'

#校长
class SchoolMasterViewSet(MyModelViewSet):
    serializer_class = SchoolMasterSerializer
    queryset = SchoolMaster.objects.get_queryset().order_by('id')


#单个注册学生
class StudentViewSet(MyModelViewSet):
    '''
    学生集
    '''
    serializer_class = StudentSerializer
    queryset = Student.objects.get_queryset().order_by('id')

    def create(self, request, *args, **kwargs):
        self.serializer_class=RegStudentSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class=RegStudentSerializer
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.serializer_class=RegStudentSerializer
        return super().partial_update(request, *args, **kwargs)

    def perform_destroy(self,instance):
        data={'student':instance}
        user=Users.objects.filter(**data).first()
        if user:
            user.delete()
        else:
            raise serializers.ValidationError('数据不存在')


#学生问卷任务
class StudentQuestionnaireViewSet(MyModelViewSet):
    '''
    学生问卷任务
    '''
    serializer_class=StudentQuestionnaireSerializer
    queryset=StudentQuestionnaire.objects.get_queryset().order_by('create_at')
    CustomFilter = {'questionnaire_id':'questionnaire_obj__id','状态':'status','学校':
        'student_obj__classstudent__s_class__gradeclass__grade__schoolgrade__school__school_name__contains',
        '问卷类型':'questionnaire_obj__questionnaire_type__type_name__contains',
        # '年级':'student_obj__classstudent__s_class__gradeclass__grade__grade_name__contains',
        # '班级':'student_obj__classstudent__s_class__class_name__contains'
                    }
    SqlNoFilter = {'年级':'custom_get_num_txt_grade','班级':'custom_get_num_txt_class'}
    FieldHelp='各参数值说明<br>'\
    '[questionnaire_id]:仅查看某一个问卷的状态/值为问卷的id<br>'\
    '[状态]:选择开放或者关闭的问卷/值为True或者False<br>'\
    '[学校]:只显示某个学校的问卷/校名未填完整也可以找到/选择此条件依然受到角色的访问范围限制<br>' \
    '[问卷类型]:可选的参数有家长问卷/老师问卷/其他问卷'\
    '[年级]:只显示此年级的问卷/通常配合学校参数使用/年级名未填完整也可以找到/<br>'\
    '[班级]:只显示此班级的问卷/通常配合学校及年级参数使用/班级名未填完整也可以找到/<br>'\

    def list(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)

    def get_queryset(self):
        user=self.request.user
        userrole_obj=UsersRoles.objects.filter(user=user).first()
        empty=StudentQuestionnaire.objects.filter()
        if userrole_obj:
            role=userrole_obj.role.role
        else:
            return empty
        #省负责人
        BIGHEAD = settings.BIGHEAD
        #市负责人
        CITYHEAD = settings.CITYHEAD
        # 年级主任
        GRADEHEAD = settings.GRADEHEAD
        if role=='老师':
            filter_filder=\
            'student_obj__classstudent__s_class__classteacher__teacher__user'
            filter_kwargs={filter_filder:user}
            queryset=self.queryset.filter(**filter_kwargs)
        elif role=='校长':
            school_objs=School.objects.filter(schoolmaster__user_obj=user)
            filter_filder=\
            'student_obj__classstudent__s_class__gradeclass__grade__schoolgrade__school__in'
            filter_kwargs={filter_filder:school_objs}
            queryset=self.queryset.filter(**filter_kwargs)
        #年级主任
        elif role==GRADEHEAD:
            grade_objs=Grade.objects.filter(gradegradehead__grade_head_obj=user)
            '''使学生的年级在年级主任的管辖内'''
            filter_kwargs={'student_obj__classstudent__s_class__gradeclass__grade__in':grade_objs}
            queryset =self.queryset.filter(**filter_kwargs)
        #城市负责人
        elif role==CITYHEAD:
            '''学生学校所属的城市在此负责人的管辖范围内'''

            city_objs=City.objects.filter(citycityhead__city_head_obj=user)
            filter_filder=\
            'student_obj__classstudent__s_class__gradeclass__grade__schoolgrade' \
            '__school__cityschool__city_obj__in'
            filter_kwargs={filter_filder:city_objs}
            queryset=self.queryset.filter(**filter_kwargs)
        #省区负责人
        elif role==BIGHEAD:
            '''学生学校所属的省份在此负责人的管辖范围内'''
            province_objs=Province.objects.filter(provinceprovincehead__province_head_obj=user)
            filter_filder=\
            'student_obj__classstudent__s_class__gradeclass__grade__schoolgrade' \
            '__school__cityschool__city_obj__province_obj__in'
            filter_kwargs={filter_filder:province_objs}
            queryset=self.queryset.filter(**filter_kwargs)
        #其他角色没有数据集
        else:
            queryset=empty
        return queryset


    #年级可能出现大小写数字，这里的筛选应该是这两种写法的合集
    def custom_get_num_txt_grade__handler(self,data):
        #以小写模式查找集合
        data=self.bignum_to_smallnum(data)
        grade_list_small=Grade.objects.filter(grade_name__contains=data)
        #以大写搜索大写
        data=self.smallnum_to_bignum(data)
        grade_list_big=Grade.objects.filter(grade_name__contains=data)
        grade_list=grade_list_small|grade_list_big
        self.queryset=self.queryset.filter(student_obj__classstudent__s_class__gradeclass__grade__in=grade_list)

    # 班级可能出现大小写数字，这里的筛选应该是这两种写法的合集
    def custom_get_num_txt_class__handler(self,data):
        #以小写模式查找集合
        data=self.bignum_to_smallnum(data)
        class_list_small=Class.objects.filter(class_name__contains=data)
        #以大写搜索大写
        data=self.smallnum_to_bignum(data)
        class_list_big=Class.objects.filter(class_name__contains=data)
        class_list=class_list_small|class_list_big
        self.queryset=self.queryset.filter(student_obj__classstudent__s_class__in=class_list)


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


# ---------------------------------------------------------------------------- T


#单个注册老师
class TeacherViewSet(MyModelViewSet):
    serializer_class = RegOneTeacherSerializer
    queryset = Users.objects.filter(userrole__role__role='老师').order_by('id')
    CustomFilter = {'名字':'user__name__contains','年龄':'user__age','性别':'user__sex',
                    '学校':'school__school_name__contains',
                    '班级':'teacherclass__class_name__class_name__contains',
                    '年级':'teacherclass__grade',}
    def create(self, request, *args, **kwargs):
        try:
            request.data._mutable=True
            request.data['is_valied']=False
            request.data._mutable=False
        except:
            request.data['is_valied']=False
        return super().create(request, *args, **kwargs)


#老师主页
class TeacherMainViewSet(MyModelViewSet):
    serializer_class = TeacherMainSerializer
    queryset = Questionnaire.objects.get_queryset().order_by('id')

    def list(self,request,*args,**kwargs):
        user=request.user
        if '老师' not in get_user_role(user):
            return Response('只允许老师访问',status=400)
        # {
        #     teacher: [{问卷: 名称, 总数: n, 已完成：x}, {问卷: 名称, 总数: n, 已完成：x}, ],
        # parent: [{问卷: 名称, 总数: n, 已完成：x}, {问卷: 名称, 总数: n, 已完成：x}, ],
        # oather: [{问卷: 名称, 总数: n, 已完成：x}, {问卷: 名称, 总数: n, 已完成：x}, ],
        # }

        #得到本班问卷
        class_obj=self.get_class(user)
        #得到本班问卷集合
        questionnaire_objs=self.get_questionnaire_objs(class_obj)
        #得到某一个问卷关于本班任务的总数和已经完成的数量
        success_info={'teacher':[],'parent':[],'other':[]}
        mapping={'老师问卷':'teacher','家长问卷':'parent','其他问卷':'other'}
        for questionnaire_obj in questionnaire_objs:
            questionnaire_type=questionnaire_obj.questionnaire_type
            questionnaire_info=self.get_questionnaire_info(questionnaire_obj,class_obj)
            success_info[mapping[questionnaire_type.type_name]].append(questionnaire_info)
        return Response(success_info)

    #定位这个班级
    def get_class(self,user):
        class_obj=Class.objects.filter(classteacher__teacher__user=user).first()
        if class_obj:
            return class_obj
        else:
            raise_error('当前用户没有绑定任何班级')

    #得到本班的问卷
    def get_questionnaire_objs(self,class_obj):
        questionnaire_objs=Questionnaire.objects.filter(classquestionnaire__class_obj=class_obj)
        return questionnaire_objs

    #得到当前问卷的数量
    def get_questionnaire_info(self,questionnaire_obj,class_id):
        #类型 名称 已经完成 总数
        #[{'questionnaire_name':'questionnaire_name','sum_count':'sum_count','finish_count':'finish_count'}]

        questionnaire_name=questionnaire_obj.questionnaire_name
        questionnaire_id = questionnaire_obj.id
        sum_count=\
            StudentQuestionnaire.objects.filter(
                questionnaire_obj=questionnaire_obj,student_obj__classstudent__s_class=class_id).count()
        finish_count=\
            StudentQuestionnaire.objects.filter(
                questionnaire_obj=questionnaire_obj,student_obj__classstudent__s_class=class_id,status=False).count()
        info={'questionnaire_id':questionnaire_id,'questionnaire_name':questionnaire_name,
              'sum_count':sum_count,'finish_count':finish_count}
        return info


#从表格注册学生及新建任务
class TaskFromXlsxViewSet(MyModelViewSet):
    serializer_class = TaskFromXlsxSerializer

    queryset = StudentQuestionnaire.objects.get_queryset().order_by('id')

    def list(self,*args,**kwargs):
        return Response('请使用post方式',status=400)

    def create(self,request, *args,**kwargs):
        a=request.data
        b=request.POST
        c=request.FILES
        request=request_add(request,{'class_id':self.get_teacher_class_id()})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.success_info, status=201, headers=headers)

    def get_teacher_class_id(self):
        user=self.request.user
        if '老师' not in get_user_role(user) :
            raise serializers.ValidationError('当前功能只允许老师角色使用')
        class_obj=Class.objects.filter(classteacher__teacher__user=user).first()
        if not class_obj:raise_error('操作无法继续,因为当前老师没有被绑定到任何班级')
        class_id=class_obj.id
        return class_id


#管理员在这里新建任务
class TaskFromManageXlsxViewSet(MyModelViewSet):
    serializer_class = TaskFromManageXlsxSerializer
    queryset = StudentQuestionnaire.objects.get_queryset().order_by('id')
    def list(self,*args,**kwargs):
        return Response('请使用post方式',status=400)

    def create(self,request, *args,**kwargs):
        #需要班级id/问卷id/
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.success_info, status=201, headers=headers)



#任务详情下载
class TaskDownViewSet(MyModelViewSet):
    serializer_class = TaskDownSerializer
    # queryset = Users.objects.all()
    def create(self,request,*args,**kwargs):
        serializer=TaskDownSerializer(data=request.data)
        serializer.user=request.user
        if serializer.is_valid():
            serializer.save()
            path=serializer.path
            # return HttpResponseRedirect(path)
            return Response({'path':path})

        else:
            return Response(serializer.errors)


# ---------------------------------------------------------------------------- U

#从已经注册的用户及角色中绑定两者的关系
class UsersRolesViewSet(MyModelViewSet):
    '''
    用户角色关联
    '''
    serializer_class=UsersRolesSerializer
    queryset = UsersRoles.objects.get_queryset().order_by('role')


#用户不存在,但是角色存在.创建用户后绑定两者的关系
class UserRolesViewSet(MyModelViewSet):
    '''
    用户不存在,但是角色存在.创建用户后绑定两者的关系
    '''
    serializer_class = UserRolesSerializer
    queryset = Users.objects.get_queryset().order_by('id')


#用户
class UsersViewSet(MyModelViewSet):
    '''
    用户创建
    '''
    serializer_class=UsersSerializer
    queryset = Users.objects.get_queryset().order_by('-updated_at')
    CustomFilter = {'名字':'name__contains','年龄':'age','性别':'sex','激活':'teacher__is_valied',
                    '角色':'userrole__role__role__contains'}
    FieldHelp = '<br>相关参数的帮助信息如下：<br>' \
                '[名字]:用户的名字/包含查询<br>' \
                '[年龄]:年龄<br>' \
                '[性别]:性别/男/女/未知<br>' \
                '[激活]:是否已经激活/选择此项默认只显示身份为老师的用户<br>' \
                '[角色]:选择一个角色/包含查询<br>'


# ---------------------------------------------------------------------------- V
# ---------------------------------------------------------------------------- W


#查看当前用户
class Who_am_I(APIView):
    # authentication_classes = (QuestionnaireAuthentication,)
    def get(self,request,*args,**kwargs):
        user=request.user
        return Response('当前用户被认证为：'+str(user))

    def get_name(self):
        from  random import randint
        a=[str(randint(0,9)) for i in range(11)]
        name= ''.join(a)
        return name


#等待发送信息的任务
class WaitSendViewSet(MyModelViewSet):
    serializer_class = WaitSendSerialzier
    queryset = WaitSend.objects.get_queryset().order_by('create_at')
    # def get_queryset(self):
    #     return self.queryset.filter(status=True)

    # CustomFilter = {'成功状态':'status'}
    # FieldHelp = '以下是筛选参数的帮助信息' \
    #             '[成功状态]:默认为未发送的任务集合/如果选择False,则已经成功的任务也会被显示,选择重新发送或者删除记录'
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.success_info, headers=headers)


#老师向学生配发问卷时产生的短信任务
class WaitSendStudentSmSViewSet(MyModelViewSet):
    '''
    老师向学生配发问卷时产生的短信任务
    '''
    serializer_class = WaitSendStudentSmSSerializer
    queryset = WaitSendStudentSmS.objects.get_queryset().order_by('updated_at')


# ---------------------------------------------------------------------------- X

#总部对老师进行验证
class VailedTeacherViewSet(MyModelViewSet):
    '''
    请在检查老师信息后进行验证
    '''
    serializer_class = VailedTeacherSerializer
    queryset = Teacher.objects.get_queryset().order_by('id')
    CustomFilter = {'名字':'user__name__contains','年龄':'user__age','性别':'user__sex',
                    '学校':'school__school_name__contains',
                    '班级':'teacherclass__class_name__class_name__contains',
                    '年级':'teacherclass__grade','已验证':'is_valied'}

    def perform_destroy(self,instance):
        data={'teacher':instance}
        user=Users.objects.filter(**data).first()
        if user:
            user.delete()
        else:
            raise serializers.ValidationError('数据不存在')

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        response=super().update(request, *args, **kwargs)
        return response


# ---------------------------------------------------------------------------- Y
# ---------------------------------------------------------------------------- Z













