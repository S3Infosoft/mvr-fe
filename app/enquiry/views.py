from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def ota_list(request):
    return render(request, "enquiry/ota_list.html")


@login_required
def partner_list(request):
    return render(request, "enquiry/partner_list.html")


@login_required
def review_list(request):
    return render(request, "enquiry/review_list.html")
