from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def activity_log(request):
    return render(request, "schedules/activity_log.html")
