from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from main.models import Elements, IonizationEnergy


def login_view(request):
    post = request.POST
    if post:
        username = post.get('username')
        password = post.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Redirect to a success page.
            return redirect('admin')
        else:
            return render(request, 'admin/login.html', locals())
    return render(request, 'admin/login.html')


def logout_view(request):
    logout(request)
    return redirect('admin')


@login_required(login_url='/admin/login/')
def index(request):
    return render(request, 'admin/admin.html')


def console(request):
    return render(request, 'admin/console.html')


def ele_list(request):
    list_name = '元素'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = Elements.objects.all().values('id', 'cn_name', 'symbol')
        count = elements_list.count()
        elements_list = elements_list[limit*(page-1): limit*page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = Elements.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_list.html', locals())


def ele_mod(request, action):
    list_name = '元素'
    post = request.POST
    eid = request.GET.get("id")
    if post:
        symbol = post.get('symbol')
        atomic_number = post.get('atomic_number')
        relative_atomic_mass = post.get('relative_atomic_mass')
        atomic_radius = post.get('atomic_radius')
        electronegativity = post.get('electronegativity')
        electronic_affinity = post.get('electronic_affinity')
        introduction = post.get('introduction')
        ionizationenergy = post.get('ionizationenergy')
        ie_list = []
        if ionizationenergy:
            ie_list = ionizationenergy.split(',')
        extra = post.get('extra')
        cn_name = post.get('cn_name')
        if action == 'add':
            ele = Elements.objects.create(symbol=symbol, atomic_number=atomic_number, relative_atomic_mass=relative_atomic_mass,
                                        atomic_radius=atomic_radius, electronegativity=electronegativity, electronic_affinity=electronic_affinity,
                                        introduction=introduction, extra=extra, cn_name=cn_name)
            for i in ie_list:
                IonizationEnergy.objects.create(ele=ele, energy=i)
            return JsonResponse({"code": 0, "msg": "add_success"})
        elif action == 'edit':
            if eid:
                Elements.objects.filter(pk=eid).update(symbol=symbol, atomic_number=atomic_number, relative_atomic_mass=relative_atomic_mass,
                                                       atomic_radius=atomic_radius, electronegativity=electronegativity, electronic_affinity=electronic_affinity,
                                                       introduction=introduction, extra=extra, cn_name=cn_name)
                IonizationEnergy.objects.filter(ele_id=eid).delete()
                for i in ie_list:
                    IonizationEnergy.objects.create(ele_id=eid, energy=i)
                return JsonResponse({"code": 0, "msg": "edit_success"})
    if action == 'edit':
        if eid:
            ele = Elements.objects.get(pk=eid)
            ie_list = IonizationEnergy.objects.filter(ele_id=eid)
            ionizationenergy_list = []
            for i in ie_list:
                ionizationenergy_list.append(i.energy)
            ionizationenergy = ','.join(ionizationenergy_list)
    return render(request, 'admin/ele_form.html', locals())
