from . import views
from django.urls import path

app_name = "enquiry"

urlpatterns = [
    path("ota/", views.ota_list, name="ota"),
    path("partner/", views.partner_list, name="partner"),
    path("review/", views.review_list, name="review"),
]
