from . import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()

router.register("ota", views.OTAViewset)
router.register("partner", views.PartnerViewSet)
router.register("review", views.ReviewViewSet)

urlpatterns = [
    path("report/", views.ReportAPIView.as_view(), name="api_report"),
    path("log/", views.ActivityListAPIView.as_view(),
         name="activity_log"),
    path("", include(router.urls)),
]
