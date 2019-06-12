from . import views
from django.urls import path, include

app_name = "enquiry"

jquery_links = [
    path("ota/", views.ota_list, name="jquery-ota"),
    path("partner/", views.partner_list, name="jquery-partner"),
    path("review/", views.review_list, name="jquery-review"),
]

urlpatterns = [
    path("j/", include(jquery_links)),
    path("ota/", views.ota_list, name="ota"),
    path("partner/", views.partner_list, name="partner"),
    path("review/", views.review_list, name="review"),
]
