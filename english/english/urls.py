from django.conf.urls import url,include
from Main.main_urls import main_router
from django.conf import settings
from django.views.static import serve

def test(request):
    from django.http import HttpResponse
    return HttpResponse('已执行')

urlpatterns = [
    url(r'^main/',include(main_router.urls)),     #关于主页面的一切路由
    # url(r'^static/(?P<path>.+)$',serve,{"document_root":settings.STATIC_ROOT}),  #uwsgi静态文件夹配置
    # url(r'')
]
