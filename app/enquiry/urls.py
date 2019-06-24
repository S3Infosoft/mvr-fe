from . import views
from django.urls import path, include

app_name = "enquiry"

ota_links = [
    path("<int:pk>/delete/", views.OTADeleteView.as_view(), name="ota_delete"),
    path("<int:pk>/", views.OTAUpdateView.as_view(), name="ota_detail"),
    path("", views.ota_list, name="ota")
]

partner_links = [
    path("<int:pk>/delete/", views.PartnerDeleteView.as_view(),
         name="partner_delete"),
    path("<int:pk>/", views.PartnerUpdateView.as_view(),
         name="partner_detail"),
    path("", views.partner_list, name="partner"),
]

review_links = [
    path("<int:pk>/delete/", views.ReviewDeleteView.as_view(),
         name="review_delete"),
    path("<int:pk>/", views.ReviewUpdateView.as_view(), name="review_detail"),
    path("", views.review_list, name="review"),
]

urlpatterns = [
    path("csv/<s_day>/<s_month>/<s_year>/<e_day>/"
         "<e_month>/<e_year>/<str:model>/",
         views.export_csv, name="csv"),
    path("pdf/<s_day>/<s_month>/<s_year>/<e_day>/"
         "<e_month>/<e_year>/<str:model>/",
         views.export_pdf, name="pdf"),
    path("report/", views.generate_report, name="report"),
    path("ota/", include(ota_links)),
    path("partner/", include(partner_links)),
    path("review/", include(review_links)),
]
