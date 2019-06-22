from . import forms

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def ota_list(request):
    if request.is_ajax():
        return render(request, "enquiry/jquery_snippets/ota_list_jquery.html")
    return render(request, "enquiry/ota_list.html", {"form": forms.OTAForm()})


@login_required
def partner_list(request):
    if request.is_ajax():
        return render(request,
                      "enquiry/jquery_snippets/partner_list_jquery.html")
    return render(request, "enquiry/partner_list.html",
                  {"form": forms.PartnerForm()})


@login_required
def review_list(request):
    if request.is_ajax():
        return render(request,
                      "enquiry/jquery_snippets/review_list_jquery.html")
    return render(request, "enquiry/review_list.html",
                  {"form": forms.ReviewForm()})
