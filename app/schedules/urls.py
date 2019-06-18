from . import views
from django.urls import path

app_name = "schedule"

urlpatterns = [
    path("activity-log/", views.activity_log, name="activity-log")
]
