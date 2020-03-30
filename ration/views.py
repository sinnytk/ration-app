from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    user = request.user
    return render(request, "ration/homepage.html", context={'page_name':"Dashboard"})
@login_required
def add_record(request):
    return render(request, "ration/add_record.html", context={'page_name':"Add Record"})
@login_required
def search_record(request):
    return render(request, "ration/search_record.html", context={'page_name':"Search Record"})
    