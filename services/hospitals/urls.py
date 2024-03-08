from rest_framework.routers import DefaultRouter
from services.hospitals.api.v1.endpoints import HospitalAPIView

app_name = 'hospitals'

router = DefaultRouter()
router.register('', HospitalAPIView, 'hospitals')

urlpatterns = [
    
]
urlpatterns += router.urls
