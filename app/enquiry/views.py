from django.shortcuts import render


def ota_list(request):
    return render(request, "enquiry/ota_list.html")


def partner_list(request):
    return render(request, "enquiry/partner_list.html")


def review_list(request):
    return render(request, "enquiry/review_list.html")
