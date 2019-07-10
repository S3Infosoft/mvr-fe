from . import forms
from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

import requests


@login_required
def schedule(request):
    if request.method == "POST":
        form = forms.ScheduleHandlingForm(request.POST)
        if form.is_valid():
            form.instance.creator = request.user
            form.save()
            cd = form.cleaned_data
            search_text = request.POST.get("search_text")
            ota = cd["ota_name"].name
            check_in_date = cd["check_in_date"].date().strftime("%d/%m/%Y")
            check_out_date = cd["check_out_date"].date().strftime("%d/%m/%Y")

            data = f'{{"search_text":"{search_text}", "checkin_date": ' \
                   f'"{check_in_date}", "checkout_date": "{check_out_date}" }}'
            headers = {'Content-Type': 'application/json'}
            url = "http://mvr-fe_mvrautomation_1:5000/automation/v1/{}".format(
                ota.lower()
            )
            form.instance.creator = request.user
            form.save()

            res = requests.post(url, headers=headers, data=data)
            return HttpResponse(res.content)
    else:
        form = forms.ScheduleHandlingForm()
    return render(request,
                  "schedules/schedule_handling.html",
                  {"form": form})


@login_required
def display_schedule(request):
    return render(request, "schedules/scheduled.html")
