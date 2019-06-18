from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("schedule/", include("schedules.urls", namespace="schedule")),
    path("enquiry/", include("enquiry.urls", namespace="enquiry")),
    path('admin/', admin.site.urls),
    path("api/v1/", include("enquiry.api.urls")),
    path("", include("users.urls")),
]

