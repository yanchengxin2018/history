from rest_framework.routers import DefaultRouter
from Main import views


main_router=DefaultRouter()
main_router.register('word',views.WordViewSet,base_name='main_word')
main_router.register('part',views.PartViewSet,base_name='main_part')
main_router.register('wordcard',views.WordCardViewSet,base_name='main_wordcard')
main_router.register('register_or_login',views.LoginOrRegisterViewSet,base_name='main_register_or_login')
main_router.register('register',views.RegisterViewSet,base_name='main_register')
main_router.register('login',views.LoginViewSet,base_name='main_login')
main_router.register('main',views.MainViewSet,base_name='main_main')

#决策器
main_router.register('decisioner',views.DecisionerViewSet,base_name='main_decisioner')
main_router.register('start',views.StartViewSet,base_name='main_start')
main_router.register('setting',views.SettingViewSet,base_name='main_setting')
main_router.register('familiar',views.FamiliarViewSet,base_name='main_familiar')
main_router.register('count',views.CountViewSet,base_name='main_count')
main_router.register('part',views.PartViewSet,base_name='main_part')
main_router.register('help',views.HelpViewSet,base_name='main_help')


main_router.register('errorword',views.ErrorWordViewSet,base_name='main_errorword')



