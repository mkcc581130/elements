from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import ensure_csrf_cookie
import pytz
import datetime
from main.models import Elements
# Create your views here.


@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')


@ensure_csrf_cookie
def ele_info(request):
    symbol = request.GET.get("symbol")
    ele = Elements.objects.get(symbol=symbol)
    ie_list = []
    cn_num = ['一', '二', '三', '四', '五']
    ionizationenergy = ele.ionizationenergy_set.all()
    if len(ionizationenergy) == 1:
        ie_list.append({'label': '电离能', 'energy': ionizationenergy[0].energy})
    else:
        for i in range(len(ionizationenergy)):
            ie_list.append({'label': '第' + cn_num[i] + '电离能', 'energy': ionizationenergy[i].energy})
    return render(request, 'element/ele_info.html', {'ele': ele, 'ie_list': ie_list})
