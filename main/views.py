from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
import pytz
import datetime
from .models import Elements,HiElements, HiElementItems, ElementHistory, ElementRepresentative, ElementRepresentativeItem, ElementIsotope
from .comm import visit_count, re_find
# Create your views here.


@visit_count
def index(request):
    return render(request, 'index.html')


def ele_info(request):
    symbol = request.GET.get("symbol")
    ele = Elements.objects.get(symbol=symbol)
    next_ele = Elements.objects.filter(atomic_number=ele.atomic_number+1)
    pre_ele = Elements.objects.filter(atomic_number=ele.atomic_number-1)
    ie_list = []
    cn_num = ['一', '二', '三', '四', '五']
    ionizationenergy = ele.ionizationenergy_set.all()
    if len(ionizationenergy) == 1:
        ie_list.append({'label': '电离能', 'energy': ionizationenergy[0].energy})
    else:
        for i in range(len(ionizationenergy)):
            ie_list.append({'label': '第' + cn_num[i] + '电离能', 'energy': ionizationenergy[i].energy})
    return render(request, 'element/ele_info.html', locals())


def hi_ele(request):
    symbol = request.GET.get("symbol")
    hiele = HiElements.objects.get(ele__symbol=symbol)
    next_ele = Elements.objects.filter(atomic_number=hiele.ele.atomic_number + 1)
    pre_ele = Elements.objects.filter(atomic_number=hiele.ele.atomic_number - 1)
    hiele_item = HiElementItems.objects.filter(ele_id=hiele.ele_id)
    return render(request, 'element/hi_ele.html', locals())


def ele_history(request):
    symbol = request.GET.get("symbol")
    ele = Elements.objects.get(symbol=symbol)
    hisele = ElementHistory.objects.filter(ele_id=ele.id).order_by('sort')
    for h in hisele:
        if h.img:
            h.img = h.img.split('，')
    next_ele = Elements.objects.filter(atomic_number=ele.atomic_number + 1)
    pre_ele = Elements.objects.filter(atomic_number=ele.atomic_number - 1)
    return render(request, 'element/ele_history.html', locals())


def ele_representative(request):
    symbol = request.GET.get("symbol")
    ele = Elements.objects.get(symbol=symbol)
    ere = ElementRepresentative.objects.get(ele_id=ele.id)
    item_list = ElementRepresentativeItem.objects.filter(representative_id=ere.id)
    duty_list = ere.duty.split("|")
    for i in item_list:
        if i.img_info:
            img_info_list = i.img_info.split('|')
            img_list = []
            for im in img_info_list:
                if im:
                    li = re_find('^(.*?) 说明：(.*?)$', im)
                    img_list.append({'img': li[0], 'explain': li[1]})
            i.img_list = img_list
            i.length = len(img_info_list)
    next_ele = Elements.objects.filter(atomic_number=ele.atomic_number + 1)
    pre_ele = Elements.objects.filter(atomic_number=ele.atomic_number - 1)
    return render(request, 'element/ele_representative.html', locals())


def ele_isotope(request):
    symbol = request.GET.get("symbol")
    ele = Elements.objects.get(symbol=symbol)
    eie = ElementIsotope.objects.get(ele_id=ele.id)
    stable_isotope_list = eie.stable_isotope.split('|')
    stable_list = []
    for s in stable_isotope_list:
        li = re_find('^(.*?) 相对原子质量：(.*?) 摩尔分数：(.*?)$', s)
        stable_list.append([li[0], li[1], li[2]])
    next_ele = Elements.objects.filter(atomic_number=ele.atomic_number + 1)
    pre_ele = Elements.objects.filter(atomic_number=ele.atomic_number - 1)
    return render(request, 'element/ele_isotope.html', locals())
