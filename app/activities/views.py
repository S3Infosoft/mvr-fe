from . import forms, utils

from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import decorators
from django.core.mail import EmailMessage
from django.http.response import HttpResponse, HttpResponseRedirect

from datetime import datetime


@decorators.login_required
def send_report_email(request, s_day, s_month, s_year,
                      e_day, e_month, e_year, model):
    start_date = datetime(year=s_year, month=s_month, day=s_day).date()
    end_date = datetime(year=e_year, month=e_month, day=e_day).date()

    if request.method == "POST":
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

            csv = utils.generate_csv(start_date, end_date, model)
            pdf = utils.generate_pdf(start_date, end_date, model)

            name = f"{model}-{start_date} {end_date}"

            email.attach(f"{name}.csv",
                         csv.csv,
                         "text/csv")
            email.attach(f"{name}.pdf",
                         pdf.getvalue(),
                         "text/pdf")
            email.send()

            return HttpResponseRedirect(reverse_lazy("activity:report"))
        else:
            print(form.errors)

    return HttpResponse("Error in email sending.")


@decorators.login_required
def export_csv(request, s_day, s_month, s_year, e_day, e_month, e_year, model):
    start_date = datetime(year=s_year, month=s_month, day=s_day).date()
    end_date = datetime(year=e_year, month=e_month, day=e_day).date()

    csv = utils.generate_csv(start_date, end_date, model)

    name = f"{model}-{start_date} {end_date}"
    res = HttpResponse(csv.csv, content_type="text/csv")
    res["Content-Disposition"] = f"attachment; filename={name}.csv"
    return res


@decorators.login_required
def export_pdf(request, s_day, s_month, s_year, e_day, e_month, e_year, model):
    start_date = datetime(year=s_year, month=s_month, day=s_day).date()
    end_date = datetime(year=e_year, month=e_month, day=e_day).date()

    pdf = utils.generate_pdf(start_date, end_date, model)

    name = f"{model}-{start_date} {end_date}"
    res = HttpResponse(pdf.getvalue(), content_type="text/pdf")
    res["Content-Disposition"] = f"attachment; filename={name}.pdf"
    return res


@decorators.login_required
def generate_report(request):
    form = forms.ReportForm()
    email_form = forms.ReportEmailForm()
    return render(request, "activities/report.html",
                  {"form": form,
                   "email_form": email_form})
