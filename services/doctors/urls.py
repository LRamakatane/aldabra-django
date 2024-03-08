from services.doctors.api.v1.endpoints import DoctorAPIView
from rest_framework.routers import DefaultRouter


app_name = 'doctors'

router = DefaultRouter()
router.register('', DoctorAPIView, 'doctors')

urlpatterns = []
urlpatterns += router.urls
