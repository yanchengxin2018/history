from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet as G,mixins as M
from django.conf import settings

# 批量的分发问卷静态页面
class BatchClassQuestionnaireViewSet(G):
    def list(self,request):
        url_root=settings.ROOT_URL
        data={'url_root':url_root}
        return render(request,'batchclassquestionnaire.html',data)


#后台
class BackViewSet(G):
    def list(self,request):
        url_root=settings.ROOT_URL
        data={'url_root':url_root}
        return render(request,'back.html',data)























