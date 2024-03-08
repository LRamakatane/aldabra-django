from rest_framework.routers import DefaultRouter
from services.patients.api.v1.endpoints import PatientAPIView


app_name = "patients"

router = DefaultRouter()
router.register("", PatientAPIView, "patients")

urlpatterns = []
urlpatterns += router.urls
