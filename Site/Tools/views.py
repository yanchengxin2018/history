import os
from rest_framework.response import Response
from rest_framework.views import APIView
import threading,time
from multiprocessing import Process


def re_start_server():
    # uwsgi.reload()
    time.sleep(2)
    sh_path='/home/ubuntu/Site/Tools/re_start.sh'
    a=os.system(sh_path)
    return a


class ReStart(APIView):
    def get(self,request):
        P=Process(target=re_start_server)
        P.start()
        return Response('5秒钟后执行重启服务器')

















