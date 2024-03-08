from rest_framework.routers import DefaultRouter
from services.medical_records.api.v1.endpoints import MedicalRecordAPIView


app_name = "medical records"

router = DefaultRouter()
router.register("", MedicalRecordAPIView, "records")

urlpatterns = []
urlpatterns += router.urls
