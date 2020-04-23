from . import views
from django.urls import path, include, re_path

app_name = "enquiry"

ota_links = [
    path("<int:pk>/", views.ota_detail, name="ota_detail"),
    path("", views.ota_list, name="ota")
]

partner_links = [
    path("<int:pk>/", views.partner_detail, name="partner_detail"),
    path("", views.partner_list, name="partner"),
]

review_links = [
    path("<int:pk>/", views.review_detail, name="review_detail"),
    path("", views.review_list, name="review"),
]

urlpatterns = [
    path("payments/", views.payments_list, name="payment_list"),
    path("ota/", include(ota_links)),
    path("partner/", include(partner_links)),
    path("review/", include(review_links)),
    re_path(r"^export/excel/(?P<month>[0-9]{2})/(?P<year>[0-9]{4})/",
            views.export_master_excel, name='export_master_excel'),
    path("master/download/", views.master_download, name='master_download'),
]
