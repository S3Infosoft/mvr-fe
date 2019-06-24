from . import forms, models
from .api import serializers

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import decorators, mixins
from django.views.generic import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from rest_framework.renderers import JSONRenderer

from datetime import datetime


@decorators.login_required
def generate_report(request):
    if request.method == "POST":
        form = forms.ReportForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            enquiry = cd["enquiry_type"]
            start_date = datetime.date(cd["start_date"])
            end_date = datetime.date(cd["end_date"])

            if enquiry == "OTA":
                queryset = models.OTA.objects.filter(
                    registration__day__gte=start_date.day,
                    registration__month__gte=start_date.month,
                    registration__year__gte=start_date.year,
                    registration__day__lte=end_date.day,
                    registration__month__lte=end_date.month,
                    registration__year__lte=end_date.year,

                )
                serializer = serializers.OTASerializer(queryset, many=True)
            elif enquiry == "PARTNER":
                queryset = models.Partner.objects.filter(
                    created__day__gte=start_date.day,
                    created__month__gte=start_date.month,
                    created__year__gte=start_date.year,
                    created__day__lte=end_date.day,
                    created__month__lte=end_date.month,
                    created__year__lte=end_date.year,
                )
                serializer = serializers.PartnerSerializer(queryset, many=True)
            else:
                queryset = models.Review.objects.filter(
                    created__day__gte=start_date.day,
                    created__month__gte=start_date.month,
                    created__year__gte=start_date.year,
                    created__day__lte=end_date.day,
                    created__month__lte=end_date.month,
                    created__year__lte=end_date.year,
                )
                serializer = serializers.ReviewSerializer(queryset, many=True)

            json = JSONRenderer().render(serializer.data)
            json = json.decode("utf-8")

            return render(request, "enquiry/report.html",
                          {"json": json,
                           "type": enquiry,
                           "result": True,
                           "start_date": start_date,
                           "end_date": end_date})
    else:
        form = forms.ReportForm()

    return render(request, "enquiry/report.html", {"form": form})


class DefaultRequirments(mixins.LoginRequiredMixin, SuccessMessageMixin):
    pass


class OTAUpdateView(DefaultRequirments, UpdateView):
    model = models.OTA
    form_class = forms.OTAForm
    template_name = "enquiry/ota_detail.html"
    success_message = "OTA successfully updated."


class PartnerUpdateView(DefaultRequirments, UpdateView):
    model = models.Partner
    form_class = forms.PartnerForm
    template_name = "enquiry/partner_detail.html"
    success_message = "Partner successfully updated."


class ReviewUpdateView(DefaultRequirments, UpdateView):
    model = models.Review
    form_class = forms.ReviewForm
    template_name = "enquiry/review_detail.html"
    success_message = "Review successfully updated."


class OTADeleteView(mixins.LoginRequiredMixin, DeleteView):
    model = models.OTA
    success_url = reverse_lazy("enquiry:ota")
    success_message = "OTA Successfully deleted."

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super(OTADeleteView, self).delete(request, *args, **kwargs)


class PartnerDeleteView(mixins.LoginRequiredMixin, DeleteView):
    model = models.Partner
    success_url = reverse_lazy("enquiry:partner")
    success_message = "Partner successfully deleted."

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super(PartnerDeleteView, self).delete(request, *args, **kwargs)


class ReviewDeleteView(mixins.LoginRequiredMixin, DeleteView):
    model = models.Review
    success_url = reverse_lazy("enquiry:review")
    success_message = "Review successfully deleted."

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super(ReviewDeleteView, self).delete(request, *args, **kwargs)


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
