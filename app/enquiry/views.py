from . import forms, models, resources, utils

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import decorators, mixins
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from datetime import datetime

# cache key format <model name in uppercase>-<start-date>-<end-date>


def generate_csv(start_date: datetime.date,
                 end_date: datetime.date,
                 model: str):

    # keys to get data from cache
    key = f"{model}-{start_date}-{end_date}"

    q = cache.get(key)

    if not q:
        # pr is the import-export object for respective model
        if model == "OTA":
            pr = resources.OTAResource()
            q = models.OTA.objects.filter(registration__date__gte=start_date,
                                          registration__date__lte=end_date)
        elif model == "PARTNER":
            pr = resources.PartnerResource()
            q = models.Partner.objects.filter(created__date__gte=start_date,
                                              created__date__lte=end_date)
        else:
            pr = resources.ReviewResource()
            q = models.Review.objects.filter(created__date__gte=start_date,
                                             created__date__lte=end_date)
        cache.set(key, q)
    else:
        if model == "OTA":
            pr = resources.OTAResource()
        elif model == "PARTNER":
            pr = resources.PartnerResource()
        else:
            pr = resources.ReviewResource()

    csv = pr.export(q)
    return csv


def generate_pdf(start_date: datetime.date,
                 end_date: datetime.date,
                 model: str):
    key = f"{model}-{start_date}-{end_date}"

    q = cache.get(key)

    if not q:
        if model == "OTA":
            q = models.OTA.objects.filter(registration__date__gte=start_date,
                                          registration__date__lte=end_date)
            template = "others/ota_pdf.html"
        elif model == "PARTNER":
            q = models.Partner.objects.filter(created__date__gte=start_date,
                                              created__date__lte=end_date)
            template = "others/partner_pdf.html"
        else:
            q = models.Review.objects.filter(created__date__gte=start_date,
                                             created__date__lte=end_date)
            template = "others/review_pdf.html"

        cache.set(key, q)
    else:
        if model == "OTA":
            template = "others/ota_pdf.html"
        elif model == "PARTNER":
            template = "others/partner_pdf.html"
        else:
            template = "others/review_pdf.html"

    pdf = utils.render_to_pdf(template, {"objects": q,
                                         "title": model,
                                         "start_date": start_date,
                                         "end_date": end_date})
    return pdf


@decorators.login_required
def send_report_email(request, s_day, s_month, s_year,
                      e_day, e_month, e_year, model):
    start_date = datetime(year=s_year, month=s_month, day=s_day).date()
    end_date = datetime(year=e_year, month=e_month, day=e_day).date()

    if request.method == "POST":
        print("started")
        form = forms.ReportEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd["subject"]
            message = cd["message"]
            sender = request.user.email
            recipient = cd["to"]

            email = EmailMessage(
                subject,
                message,
                sender,
                [recipient])

            csv = generate_csv(start_date, end_date, model)
            pdf = generate_pdf(start_date, end_date, model)

            name = f"{model}-{start_date} {end_date}"

            email.attach(f"{name}.csv",
                         csv.csv,
                         "text/csv")
            email.attach(f"{name}.pdf",
                         pdf.getvalue(),
                         "text/pdf")
            email.send()

            return HttpResponseRedirect(reverse_lazy("enquiry:report"))
        else:
            print(form.errors)

    return HttpResponse("Error in email sending.")


@decorators.login_required
def export_csv(request, s_day, s_month, s_year, e_day, e_month, e_year, model):
    start_date = datetime(year=s_year, month=s_month, day=s_day).date()
    end_date = datetime(year=e_year, month=e_month, day=e_day).date()

    csv = generate_csv(start_date, end_date, model)

    name = f"{model}-{start_date} {end_date}"
    res = HttpResponse(csv.csv, content_type="text/csv")
    res["Content-Disposition"] = f"attachment; filename={name}.csv"
    return res


@decorators.login_required
def export_pdf(request, s_day, s_month, s_year, e_day, e_month, e_year, model):
    start_date = datetime(year=s_year, month=s_month, day=s_day).date()
    end_date = datetime(year=e_year, month=e_month, day=e_day).date()

    pdf = generate_pdf(start_date, end_date, model)

    name = f"{model}-{start_date} {end_date}"
    res = HttpResponse(pdf.getvalue(), content_type="text/pdf")
    res["Content-Disposition"] = f"attachment; filename={name}.pdf"
    return res


@decorators.login_required
def generate_report(request):
    form = forms.ReportForm()
    email_form = forms.ReportEmailForm()
    return render(request, "enquiry/report.html", {"form": form,
                                                   "email_form": email_form})


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
