from rest_framework import viewsets
from Main.serializers import *
from Main.models import *
from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet as G
from rest_framework import mixins as M
from rest_framework.response import Response
from Main.tools import get_token_from_user
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import settings
from Main.tools import decisioner_handler
from Main.permissions import IsAuthentication
import random,datetime


#所有的单词
class WordViewSet(viewsets.ModelViewSet):

    serializer_class =WordSerializer

    def get_queryset(self):
        # if not WordModel.objects.all():
        #     self.fun()
        words_obj=WordModel.objects.all()
        return words_obj.order_by('id')

    def fun(self):
        with open('english_word.txt', 'rb') as f:
            datas = f.readlines()
        for index,data in enumerate(datas):
            data = data.decode('utf8')
            word, yinbiao, wenzi=self.get_word_yibiao_wenzi(data)
            self.save_word(index,word,yinbiao,wenzi)

    def get_word_yibiao_wenzi(self,data):
        data=data.replace('[','/').replace(']','/')
        print(data)
        print(data.split('/'))
        word = data.split('/')[0].split('.')[1].strip()
        yinbiao = data.split('/')[1].strip()
        wenzi = data.split('/')[-1].replace(' ', '').strip()
        return word,yinbiao,wenzi

    def save_word(self,index,word,yinbiao,wenzi):
        WordModel.objects.create(index=index,english=word,pronunciation=yinbiao,chinese=wenzi)


#错误的的单词
class ErrorWordViewSet(viewsets.ModelViewSet):
    queryset = WordModel.objects.all().order_by('id')
    serializer_class = WordSerializer
    def get_queryset(self):
        words_obj=WordModel.objects.all()
        # return words_obj.filter(chinese__contains='有毒')
        error_words=[]
        for word_obj in words_obj:
            english=word_obj.english
            if not self.is_ok(english):
                error_words.append(word_obj.id)
        words_obj=words_obj.filter(id__in=error_words)
        return words_obj.order_by('id')


    def is_ok(self,english):
        # english='pɔisonous'
        for c in english:
            if not ((c in 'qwertyuiopasdfghjklzxcvbnm') or (c in 'QWERTYUIOPASDFGHJKLZXCVBNM')):
                # print(c,'no')
                return False
        # print('ok')
        return True
    def create(self,request,*args,**kwargs):
        alert=[
        [82,'appoint'],
        [112,'Atlantic'],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ]
        obj=WordModel.objects.get(pk=82)
        obj.english='appoint'
        obj.save()
        return Response('好了')


#
# #所有的单词零件
# class PartViewSet(viewsets.ModelViewSet):
#
#     serializer_class = PartSerializer
#
#     def get_queryset(self):
#         # if not PartModel.objects.all():
#         #     self.get_part_count()
#         parts_obj=PartModel.objects.all()
#         n=self.request.GET.get('n',None)
#         count=self.request.GET.get('count',None)
#         n_plus=self.request.GET.get('n_plus',None)
#         if n:
#             parts_list=filter(lambda part_obj:len(part_obj.part)==int(n),parts_obj)
#             parts_id=[part_obj.id for part_obj in parts_list]
#             parts_obj=parts_obj.filter(id__in=parts_id)
#         if n_plus:
#             parts_list=filter(lambda part_obj:len(part_obj.part)>=int(n_plus),parts_obj)
#             parts_id=[part_obj.id for part_obj in parts_list]
#             parts_obj=parts_obj.filter(id__in=parts_id)
#         if count:
#             parts_obj=parts_obj.filter(count__gt=int(count))
#         return parts_obj.order_by('-count')
#
#     def get_part_count(self):
#         words_obj=WordModel.objects.all()
#         l=len(words_obj)
#         for index,word_obj in enumerate(words_obj):
#             self.word_part_handler(word_obj)
#             print(f'{word_obj.english}的处理已经完成----{index}/{l}')
#
#     def word_part_handler(self,word_obj):
#         english=word_obj.english
#         for i in range(len(english)):
#             i=i+1
#             self.get_the_part_count(english,i)
#
#     def get_the_part_count(self,english,i):
#             for j in range(len(english)):
#                 if (j+i)<=len(english):
#                     part=english[j:j+i]
#                     part_obj=PartModel.objects.filter(part=part).first()
#                     if part_obj:
#                         part_obj.count=part_obj.count+1
#                         part_obj.save()
#                     else:
#                         PartModel.objects.create(part=part)
#                 else:
#                     break
#


#单词卡片页面

class WordCardViewSet(G,M.ListModelMixin):

    def list(self, request, *args, **kwargs):
        import random
        word_obj=WordModel.objects.all()[random.randint(0,100)]
        pronunciation=self.format_pronunciation(word_obj.pronunciation)
        data={"english":word_obj.english,'chinese':word_obj.chinese,
              'pronunciation':pronunciation}
        return render(request, 'start.html', data)

    def format_pronunciation(self,pronunciation):
        pronunciation=pronunciation.replace('/','')
        return '/{}/'.format(pronunciation)
        # return f"/{pronunciation}/"

#登陆注册页面
class LoginOrRegisterViewSet(G):

    def list(self,request):
        user_obj=request.user
        if user_obj:
            return render(request,'Main.html',{})
        else:
            return render(request,'register_or_login.html',{})

#注册
class RegisterViewSet(G):
    serializer_class = RegisterSerializer
    queryset = UserModel.objects.all().order_by('id')

    def list(self,request):
        return render(request,'register.html',{})

    def create(self,request):
        serializer_class=self.get_serializer_class()
        serializer_obj=serializer_class(data=request.data)
        if serializer_obj.is_valid():
            user_obj=serializer_obj.save()
            token = get_token_from_user(user_obj)
            response = HttpResponseRedirect('/main/main/')
            response.set_cookie('token', token)
            return response
        else:
            return HttpResponse(str(serializer_obj.errors))


#登陆
class LoginViewSet(G):
    serializer_class = LoginSerializer
    queryset = UserModel.objects.all().order_by('id')

    def list(self,request):
        return render(request,'login.html',{})

    def create(self,request):
        serializer_class=self.get_serializer_class()
        serializer_obj=serializer_class(data=request.data)
        if serializer_obj.is_valid():
            user_obj=serializer_obj.save()
            token = get_token_from_user(user_obj)
            response = HttpResponseRedirect('/main/main/')
            response.set_cookie('token', token)
            return response
        else:
            return HttpResponse(str(serializer_obj.errors),status=400)


#主页
class MainViewSet(G):
    queryset = UserModel.objects.all().order_by('id')
    serializer_class = UserSerializer

    def list(self,request):
        user_obj=request.user
        if user_obj:
            return render(request,'Main.html',{})
        else:
            return render(request,'register_or_login.html',{})


#开始
class StartViewSet(G):
    queryset = UserModel.objects.all().order_by('id')
    serializer_class = UserSerializer

    def list(self,request):
        if not request.user:
            return HttpResponseRedirect('/main/main/')
        return render(request, 'start.html', {})


#决策器
class DecisionerViewSet(G):
    queryset = UserModel.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = (IsAuthentication,)

    def list(self,request):
        handler=self.decisioner_handler(request.GET)
        data=handler(request.GET)
        return Response(data)

    #决策器
    def decisioner_handler(self,data):
        if not data:
            handler=self.args_null_handler
        else:
            card_type=data.get('card_type',None)
            if card_type=='test_card':
                handler =self.args_test_handler
            elif card_type=='memory_card':
                handler =self.args_memory_handler
            else:
                raise serializers.ValidationError('未知的卡片类型')
        return handler

    #处理者
    def args_null_handler(self,data):
        # 空参处理者
        word_obj=self.choice_card()
        if word_obj:
            response_data=self.get_test_data(word_obj)
        else:
            response_data =self.get_memory_data()
        return response_data

    def args_memory_handler(self,data):
        self.memory_count(data)
        return self.args_null_handler(data)

    def args_test_handler(self,data):
        status_info=self.test_count(data)
        response_data =self.get_info_data(data,status_info)
        return response_data

    #处理者工具
    def choice_card(self):
        # 卡片选择器
        # 获得所有此人记录表
        records_obj = RecordModel.objects.filter(user_obj=self.request.user)
        # 保证每个单词是唯一的并且是最后创建的
        last_record_obj = []
        for record_obj in records_obj:
            if record_obj in last_record_obj: continue
            record_obj = records_obj.filter(word_obj=record_obj.word_obj).order_by('-created_at').first()
            last_record_obj.append(record_obj)
        record_objs = last_record_obj
        # 筛选即将进行测试的单词
        test_words = []
        for record_obj in record_objs:
            # 获得单词创建时间和级别
            created_at = record_obj.created_at
            level = record_obj.level
            # 得到级别对应的测试时间
            time_long = getattr(settings, 'LEVEL_{}'.format(level))
            # 如果创建时间加测试时间小于现在,证明这个记录需要进行测试环节
            now = datetime.datetime.now()
            if created_at + time_long < now:
                test_words.append(record_obj)
        # 如果有需要测试的单词，则返回需要测试的单词
        if test_words:
            test_ids = [test_word.id for test_word in test_words]
            test_words_obj = RecordModel.objects.filter(id__in=test_ids).order_by('-created_at')
            return test_words_obj.first().word_obj
        else:
            return None

    def memory_count(self,data):
        english=data.get('english',None)
        user_obj=self.request.user
        word_obj=WordModel.objects.filter(english=english).first()
        serializer = RecordSerializer(data={'word_obj': word_obj.id, 'user_obj': user_obj.id, 'level': 0})
        if serializer.is_valid():
            serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)

    def test_count(self,data):
        return
        english=data.get('english',None)
        answer=data.get('answer',None)
        user_obj=self.request.user
        user_id=user_obj.id
        word_obj=WordModel.objects.filter(english=english).first()
        record_obj = RecordModel.objects.filter(word_obj=word_obj, user_obj=user_obj).order_by('-created_at').first()
        cai=False
        if english==answer:
            level = record_obj.level + 1
            status_info=(True,level,getattr(settings,'LEVEL_{}'.format(level)),cai)
        else:
            level = record_obj.level - 1
            if level < 0:
                cai=True
                level = 0
            status_info = (False, level,getattr(settings,'LEVEL_{}'.format(level)),cai)



        if level < 0: level = 0
        serializer = RecordSerializer(data={'word_obj': word_obj.id, 'user_obj': user_id, 'level': level})
        if serializer.is_valid():
            serializer.save()
            return status_info
        else:
            raise serializers.ValidationError(serializer.errors)

    #卡片生成器
    def get_memory_data(self):
        words_obj = WordModel.objects.all()
        word_obj = words_obj[random.randint(0, len(words_obj))]
        # english='administration'
        pronunciation = self.format_pronunciation(word_obj.pronunciation)
        data = {'card_type':'memory_card','english': word_obj.english, 'chinese': word_obj.chinese,
                'pronunciation': pronunciation}
        return data

    def get_test_data(self,word_obj):
        pronunciation = self.format_pronunciation(word_obj.pronunciation)
        data = {'card_type':'test_card',"english": word_obj.english, 'chinese': word_obj.chinese,
                'pronunciation': pronunciation}
        return data

    def get_info_data(self,data,status_info):
        success_status=status_info[0]
        level=status_info[1]
        level_1=level-(1 if success_status else -1)
        time_long=self.format_time(status_info[2])
        pronunciation=self.format_pronunciation(data["pronunciation"])

        level_info='等级{}➡等级{}'.format(level_1 if not status_info[3] else 0,level)

        data={'card_type':'info_card','success_status':success_status,
              'english':data['english'],'chinese':data['chinese'],'pronunciation':pronunciation,
              'answer':data['answer'],'level':level_info,'time':time_long,}
        return data



    def format_time(self,time_long_obj):
        time_long_list=str(time_long_obj).split(',')
        if len(time_long_list)>1:
            day=time_long_list[0].split(' ')[0]
            hms=time_long_list[1]
        else:
            day=0
            hms=time_long_list[0]
        h,m,s=hms.split(':')
        day='{}天'.format(int(day)) if int(day) else ''
        h='{}小时'.format(int(h)) if int(h) else ''
        m='{}分钟'.format(int(m)) if int(m) else ''
        s='{}秒'.format(int(s)) if int(s) else ''
        time_str=day+h+m+s
        time_long='{}后再次测试'.format(time_str)
        return time_long

    def format_pronunciation(self,pronunciation):
        pronunciation=pronunciation.replace('/','')
        return '/{}/'.format(pronunciation)


#设置
class SettingViewSet(G):
    queryset = UserModel.objects.all().order_by('id')
    serializer_class = UserSerializer

    def list(self,request):
        return Response('成功')


#熟词
class FamiliarViewSet(G):
    queryset = UserModel.objects.all().order_by('id')
    serializer_class = UserSerializer

    def list(self,request):
        return Response('成功')


#统计
class CountViewSet(G):
    queryset = UserModel.objects.all().order_by('id')
    serializer_class = UserSerializer

    def list(self,request):
        return Response('成功')


#部首
class PartViewSet(G,M.ListModelMixin):
    queryset = UserModel.objects.all().order_by('id')
    serializer_class = UserSerializer

    def list(self,request,*args,**kwargs):
        return Response('成功')


#帮助
class HelpViewSet(G):
    queryset = UserModel.objects.all().order_by('id')
    serializer_class = UserSerializer

    def list(self,request):
        return Response('成功')

















