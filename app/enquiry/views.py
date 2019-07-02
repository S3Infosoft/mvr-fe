from . import forms, models

from django.shortcuts import render
from django.contrib.auth import decorators, mixins
from django.contrib.messages.views import SuccessMessageMixin

# cache key format <model name in uppercase>-<start-date>-<end-date>


class DefaultRequirments(mixins.LoginRequiredMixin, SuccessMessageMixin):
    pass


@decorators.login_required
def ota_detail(request, pk):
    obj_data = models.OTA.objects.get(pk=pk)
    form = forms.OTAForm(instance=obj_data)
    return render(request, "enquiry/ota_detail.html", {"form": form,
                                                       "title": obj_data.name})


@decorators.login_required
def partner_detail(request, pk):
    obj_data = models.Partner.objects.get(pk=pk)
    form = forms.PartnerForm(instance=obj_data)
    return render(request, "enquiry/partner_detail.html",
                  {"form": form,
                   "title": obj_data.name})


@decorators.login_required
def review_detail(request, pk):
    obj_data = models.Review.objects.get(pk=pk)
    form = forms.ReviewForm(instance=obj_data)
    return render(request, "enquiry/review_detail.html",
                  {"form": form,
                   "title": obj_data.headline})


@decorators.login_required
def ota_list(request):
    if request.is_ajax():
        return render(request, "enquiry/jquery_snippets/ota_list_jquery.html")
    return render(request, "enquiry/ota_list.html", {"form": forms.OTAForm()})


@decorators.login_required
def partner_list(request):
    if request.is_ajax():
        return render(request,
                      "enquiry/jquery_snippets/partner_list_jquery.html")
    return render(request, "enquiry/partner_list.html",
                  {"form": forms.PartnerForm()})


@decorators.login_required
def review_list(request):
    if request.is_ajax():
        return render(request,
                      "enquiry/jquery_snippets/review_list_jquery.html")
    return render(request, "enquiry/review_list.html",
                  {"form": forms.ReviewForm()})
