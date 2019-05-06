from django.contrib.auth import get_user_model
import random
from rest_framework_jwt.settings import api_settings
from Main.models import RecordModel
from django.contrib.auth import settings
import datetime


def get_username():
    user_model=get_user_model()
    while True:
        username=[str(random.randint(0,9)) for i in range(15)]
        username=''.join(username)
        user_obj=user_model.objects.filter(username=username).first()
        if not user_obj:
            break
    return username


def password_handler(password):
    s=''
    for c in password:
        s=s+str(ord(c))
    return s


#从用户实例转化为token
def get_token_from_user(user_obj=None):
    '''
    从用户实例转化为token
    :param user_obj:用户实例
    :return:token
    '''
    payload = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode = api_settings.JWT_ENCODE_HANDLER
    data = payload(user_obj) # 把用户表转化为字典
    data['validate_sign']=user_obj.validate_sign
    token = jwt_encode(data) # 把字典转化为jwt字符串
    return token


#得到随机数量的数字字符串
def get_num(n):
    '''
    得到随机数量的数字字符串
    :param n: 要生成的随机数字字符串的长度
    :return: str类型的字符串
    '''
    return ''.join([str(random.randint(0,9)) for i in range(n)])


#决策器--决定使用单词卡还是测试卡
def decisioner_handler(user_obj):
    #获得所有此人记录表
    records_obj=RecordModel.objects.filter(user_obj=user_obj)
    #保证每个单词是唯一的并且是最后创建的
    last_record_obj=[]
    for record_obj in records_obj:
        if record_obj in last_record_obj:continue
        record_obj=records_obj.filter(word_obj=record_obj.word_obj).order_by('-created_at').first()
        last_record_obj.append(record_obj)
    record_objs=last_record_obj
    #筛选即将进行测试的单词
    test_words=[]
    for record_obj in record_objs:
        #获得单词创建时间和级别
        created_at=record_obj.created_at
        level=record_obj.level
        #得到级别对应的测试时间
        time_long=getattr(settings,'LEVEL_{}'.format(level))
        #如果创建时间加测试时间小于现在,证明这个记录需要进行测试环节
        now=datetime.datetime.now()
        if created_at+time_long<now:
            test_words.append(record_obj)
    #如果有需要测试的单词，则返回需要测试的单词集
    if test_words:
        test_ids=[test_word.id for test_word in test_words]
        test_words_obj=RecordModel.objects.filter(id__in=test_ids).order_by('-created_at')
        return test_words_obj.first().word_obj
    else:
        return None





















