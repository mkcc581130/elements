from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import ensure_csrf_cookie
import pytz
import datetime
# Create your views here.


@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')


@ensure_csrf_cookie
def ele_info(request):
    return render(request, 'element/ele_info.html')
