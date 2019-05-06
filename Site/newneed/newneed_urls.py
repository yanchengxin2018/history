from rest_framework.routers import DefaultRouter
from newneed import views

newneed_router=DefaultRouter()
newneed_router.register(r'batchclassquestionnaire',views.BatchClassQuestionnaireViewSet,base_name='batchclassquestionnaire')
newneed_router.register(r'Back',views.BackViewSet,base_name='Back')























