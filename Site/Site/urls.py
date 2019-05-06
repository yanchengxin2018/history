from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from Questionnaire import views as  Questionnaire_views
from django.conf.urls import include
from django.views.static import serve
from django.conf import settings
from django.views.generic.base import RedirectView
#Code 密码 验证
from Tools import views as tools_views
from back.urls import back_router
from role.role_urls import role_router
from newneed.newneed_urls import newneed_router

router = DefaultRouter()
#用户
router.register(r'Questionnaire_Users',Questionnaire_views.UsersViewSet)
#角色
router.register(r'Questionnaire_Roles',Questionnaire_views.RolesViewSet)
#用户角色
router.register(r'Questionnaire_UsersRoles',Questionnaire_views.UsersRolesViewSet)
#接口
router.register(r'Questionnaire_Resources',Questionnaire_views.ResourcesViewSet)
#动作
router.register(r'Questionnaire_Action',Questionnaire_views.ActionViewSet)
#权限表
router.register(r'Questionnaire_ResourceRoleAction',Questionnaire_views.ResourceRoleActionViewSet)
#验证码*
router.register(r'Questionnaire_Codes',Questionnaire_views.CodesViewSet)
#问卷
router.register(r'Questionnaire_Questionnaire',Questionnaire_views.QuestionnaireViewSet)
#问卷类型
router.register(r'Questionnaire_QuestionnaireType',Questionnaire_views.QuestionnaireTypeViewSet)
#学校
router.register(r'Questionnaire_School',Questionnaire_views.SchoolViewSet)
#年级
router.register(r'Questionnaire_Grade',Questionnaire_views.GradeViewSet)
#老师
router.register(r'Questionnaire_Teacher',Questionnaire_views.TeacherViewSet)
#班级
router.register(r'Questionnaire_Class',Questionnaire_views.ClassViewSet)
#班级老师关联
router.register(r'Questionnaire_ClassTeacher',Questionnaire_views.ClassTeacherViewSet)
#验证老师
router.register(r'Questionnaire_VailedTeacher',Questionnaire_views.VailedTeacherViewSet)
#学生
# router.register(r'Questionnaire_Student',Questionnaire_views.StudentViewSet)
#班级学生关联
# router.register(r'Questionnaire_ClassStudent',Questionnaire_views.ClassStudentViewSet)
#绑定班级和问卷
router.register(r'Questionnaire_ClassQuestionnaire',Questionnaire_views.ClassQuestionnaireViewSet)
#把问卷批量的绑定到班级
router.register(r'Questionnaire_BatchClassQuestionnaire',Questionnaire_views.BatchClassQuestionnaireViewSet)
#绑定学生和问卷
router.register(r'Questionnaire_StudentQuestionnaire',Questionnaire_views.StudentQuestionnaireViewSet)
#把问卷批量的发送给学生
router.register(r'Questionnaire_BatchStudentQuestionnaire',Questionnaire_views.BatchStudentQuestionnaireViewSet)
#校长
router.register(r'Questionnaire_SchoolMaster',Questionnaire_views.SchoolMasterViewSet)
#查看有哪些错误的提交
router.register(r'Questionnaire_ErrorCommit',Questionnaire_views.ErrorCommitViewSet)
#省
router.register(r'Questionnaire_Province',Questionnaire_views.ProvinceViewSet)
#城市
router.register(r'Questionnaire_City',Questionnaire_views.CityViewSet)
#城市学校关联
router.register(r'Questionnaire_CitySchool',Questionnaire_views.CitySchoolViewSet)
#用户不存在,但是角色存在.创建用户后绑定两者的关系
router.register(r'Questionnaire_UserRoles',Questionnaire_views.UserRolesViewSet)
#年级添加年级主任
router.register(r'Questionnaire_GradeGradeHead',Questionnaire_views.GradeGradeHeadViewSet)
# 城市添加城市负责人
router.register(r'Questionnaire_CityCityHead',Questionnaire_views.CityCityHeadViewSet)
#省添加省负责人
router.register(r'Questionnaire_ProvinceProvinceHead',Questionnaire_views.ProvinceProvinceHeadViewSet)
#等待发送信息的任务
router.register(r'Questionnaire_WaitSend',Questionnaire_views.WaitSendViewSet)
#注册老师
router.register(r'Questionnaire_RegTeacher',Questionnaire_views.RegTeacherViewSet)
#修改密码
router.register(r'Questionnaire_UserPassword',Questionnaire_views.UserPasswordViewSet)
#老师向学生配发问卷时产生的任务
router.register(r'Questionnaire_WaitSendStudentSmS',Questionnaire_views.WaitSendStudentSmSViewSet)
#从电子表格注册及添加任务
router.register(r'Questionnaire_TaskFromXlsx',Questionnaire_views.TaskFromXlsxViewSet)
#管理员从这里添加问卷
router.register(r'Questionnaire_TaskFromManageXlsx',Questionnaire_views.TaskFromManageXlsxViewSet)
#老师主页的必要信息
router.register(r'Questionnaire_TeacherMain',Questionnaire_views.TeacherMainViewSet)
#查看问卷的短信发送状态
router.register(r'Questionnaire_QuestionnaireSmsStatus',Questionnaire_views.QuestionnaireSmsStatusViewSet)
#关于这个问卷的任务进行短信通知
router.register(r'Questionnaire_QuestionnaireSmsSend',Questionnaire_views.QuestionnaireSmsSendViewSet)
#相关角色通过这个接口下载任务详情
router.register(r'Questionnaire_TaskDown',Questionnaire_views.TaskDownViewSet,base_name='task')
#通过精确的ip查找class集合
router.register(r'Questionnaire_BatchClassQuestionnaireOfId',Questionnaire_views.BatchClassQuestionnaireOfIdViewSet)


router.register(r'AAA',Questionnaire_views.AAA,base_name='xxx')


router2 = DefaultRouter()
router2.register(r'chat',Questionnaire_views.chatview)


urlpatterns = [
    url(r'^api/',include(router.urls)),
    url(r'^role/', include(role_router.urls)),
    url(r'^newneed/', include(newneed_router.urls)),
    #登入
    url(r'^user/Login/',Questionnaire_views.Login.as_view()),
    #登出
    url(r'^user/LoginOut/', Questionnaire_views.LoginOut.as_view()),
    # url(r'^Who_am_I/',Questionnaire_views.Who_am_I.as_view()),
    #批量注册老师
    url(r'^api/Questionnaire_BatchTeacher/',Questionnaire_views.BatchTeacherViewSet.as_view()),
    #批量注册学生
    url(r'^api/Questionnaire_BatchStudent/', Questionnaire_views.BatchStudentViewSet.as_view()),
    #金数据对接接口
    url(r'^api/Questionnaire_QuestionnaireMedia/',
        Questionnaire_views.QuestionnaireMediaAPIView.as_view()),
    # url(r'^del', Questionnaire_views.DelModel.as_view()),
    url(r'test',Questionnaire_views.Test.as_view(),name='ttt'),
    url(r'^$',include(router2.urls)),
    url(r'download',Questionnaire_views.download_file),
    url(r'^static/(?P<path>.+)$',serve,{"document_root":settings.STATIC_ROOT}),
    url(r'^index[/+]$',  RedirectView.as_view(url="/static/dist/index.html#/user/login")),
    url(r'^back[/+]$', RedirectView.as_view(url="/newneed/Back/")),
    url(r'teacher_muban[/+]$', RedirectView.as_view(url='{}/static/批量注册老师.xlsx'.format(settings.ROOT_URL)),),
    url(r'validate_teacher/(?P<id>[0-9]+)/(?P<password>[0-9]+)/$',Questionnaire_views.ValidateTeacherOfHrefViewSet.as_view()),
    url(r'batchclassquestionnaire/$',
        RedirectView.as_view(url='{}/static/batchclassquestionnaire.html'.format(settings.ROOT_URL)),),
    url(r'restart/',tools_views.ReStart.as_view()),
    url(r'^back_add/', include(back_router.urls)),
]









