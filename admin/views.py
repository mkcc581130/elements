import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from main.models import Elements, IonizationEnergy, VisitLog, HiElements, HiElementItems
from main.comm import re_find


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
    if 'date' in request.GET and 'type' in request.GET:
        date = request.GET.get('date')
        type = request.GET.get('type')
        sql_str = ""
        sql = ""
        if date == '1':
            sql_str = " and date_format(gmt_created, '%Y-%m-%d')=date_format(now(), '%Y-%m-%d')"
        elif date == '2':
            sql_str = " and YEARWEEK(date_format(gmt_created,'%Y-%m-%d')) = YEARWEEK(now())"
        elif date == '3':
            sql_str = " and date_format(gmt_created, '%Y-%m')=date_format(now(), '%Y-%m')"
        elif date == '4':
            sql_str = " and date_format(gmt_created, '%Y')=date_format(now(), '%Y')"
        if type == 'pv':
            sql = "select count(*) as count from main_visitlog where id>0" + sql_str
        elif type == 'uv':
            sql = "select count(*) as count from(select distinct date_format(time, '%Y-%m-%d') as date,ip from main_visitlog where id>0" + sql_str + ") a"
        elif type == 'ip':
            sql = "select count(*) as count from(select ip from main_visitlog where id>0" + sql_str + " group by ip) a"
        count = VisitLog.objects.extra(select={"count": sql}).count()
        return JsonResponse({'code': 0, 'msg': 'success', 'count': count})
    elif 'range_date' in request.GET:
        date = request.GET.get('range_date')
        sql_str = ''
        sql_arg = []
        if date == 'none':
            pv_data = VisitLog.objects.raw("select 1 as id,date_format(time, '%%Y-%%m-%%d') as date,count(*) as count from main_visitlog group by date_format(time, '%%Y-%%m-%%d') order by date_format(time, '%%Y-%%m-%%d') ")
            uv_data = VisitLog.objects.raw("select 1 as id,a.date,count(*) as count from (select distinct date_format(time, '%%Y-%%m-%%d') as date,ip from main_visitlog) a group by a.date order by a.date ")
        else:
            date_list = date.split(' - ')
            start_time = date_list[0]
            end_time = date_list[1]
            if start_time:
                sql_str += ' and gmt_created>=%s'
                sql_arg.append(start_time)
            if start_time:
                sql_str += ' and gmt_created<=%s'
                sql_arg.append(end_time + " 23:59:59")
            pv_data = VisitLog.objects.raw("select 1 as id,date_format(time, '%%Y-%%m-%%d') as date,count(*) as count from main_visitlog where id>0" + sql_str + " group by date_format(time, '%%Y-%%m-%%d') order by date_format(time, '%%Y-%%m-%%d') ", sql_arg)
            uv_data = VisitLog.objects.raw("select 1 as id,a.date,count(*) as count from (select distinct date_format(time, '%%Y-%%m-%%d') as date,ip from main_visitlog where id>0" + sql_str + ") a group by a.date order by a.date ", sql_arg)
        date = []
        PV_data = []
        UV_data = []
        for p in pv_data:
            date.append(p.date)
            PV_data.append(str(p.count))
        for u in uv_data:
            UV_data.append(str(u.count))
        return JsonResponse({'code': 0, 'msg': 'success', 'date': date, 'PV_data': PV_data, 'UV_data': UV_data})
    elif 'range_date2' in request.GET:
        date = request.GET.get('range_date2')
        sql_str = ''
        sql_arg = []
        if date == 'none':
            pv_data2 = VisitLog.objects.raw("select 1 as id,date_format(time, '%%k') as date,count(*) as count from main_visitlog where date_format(time, '%%Y-%%m-%%d')=date_format(now(), '%%Y-%%m-%%d') group by date order by date")
            uv_data2 = VisitLog.objects.raw("select 1 as id,date_format(a.time, '%%k') as date,count(*) as count from (select time,ip from main_visitlog where date_format(time, '%%Y-%%m-%%d')=date_format(now(), '%%Y-%%m-%%d') group by ip order by time) a group by date order by date")
        else:
            sql_str += " and date_format(gmt_created, '%%Y-%%m-%%d')=%s"
            sql_arg.append(date)
            pv_data2 = VisitLog.objects.raw("select 1 as id,date_format(time, '%%k') as date,count(*) as count from main_visitlog where id>0" + sql_str + " group by date order by date ", sql_arg)
            uv_data2 = VisitLog.objects.raw("select 1 as id,date_format(a.time, '%%k') as date,count(*) as count from (select time,ip from main_visitlog where id>0" + sql_str + " group by ip order by time) a group by date order by date ", sql_arg)
        date2 = []
        PV_data2 = []
        UV_data2 = []
        for i in range(0, 24):
            if i < 10:
                date2.append('0%d:00' % i)
            else:
                date2.append('%d:00' % i)
            PV_data2.append('0')
            UV_data2.append('0')
        for p in pv_data2:
            PV_data2[int(p.date)] = p.count
        for u in uv_data2:
            UV_data2[int(u.date)] = u.count
        return JsonResponse({'code': 0, 'msg': 'success', 'date2': date2, 'PV_data2': PV_data2, 'UV_data2': UV_data2})
    else:
        day_pv = VisitLog.objects.raw("select 1 as id, count(*) as count from main_visitlog where date_format(time, '%%Y-%%m-%%d')=date_format(now(), '%%Y-%%m-%%d')")[0].count
        day_uv = VisitLog.objects.raw("select 1 as id, count(*) as count from(select distinct date_format(time, '%%Y-%%m-%%d') as date,ip from main_visitlog where date_format(time, '%%Y-%%m-%%d')=date_format(now(), '%%Y-%%m-%%d')) a")[0].count
        day_ip = VisitLog.objects.raw("select 1 as id, count(*) as count from(select ip from main_visitlog where date_format(time, '%%Y-%%m-%%d')=date_format(now(), '%%Y-%%m-%%d') group by ip) a")[0].count
        all_pv = VisitLog.objects.raw("select 1 as id, count(*) as count from main_visitlog")[0].count
        all_uv = VisitLog.objects.raw("select 1 as id, count(*) as count from(select distinct date_format(time, '%%Y-%%m-%%d') as date,ip from main_visitlog) a")[0].count
        all_ip = VisitLog.objects.raw("select 1 as id, count(*) as count from(select ip from main_visitlog group by ip) a")[0].count
        return render(request, 'admin/console.html', locals())


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
        color = post.get('color')
        ie_list = []
        if ionizationenergy:
            ie_list = ionizationenergy.split('|')
        extra = post.get('extra')
        cn_name = post.get('cn_name')
        if action == 'add':
            ele = Elements.objects.create(symbol=symbol, atomic_number=atomic_number, relative_atomic_mass=relative_atomic_mass,
                                        atomic_radius=atomic_radius, electronegativity=electronegativity, electronic_affinity=electronic_affinity,
                                        introduction=introduction, extra=extra, cn_name=cn_name, color=color)
            for i in ie_list:
                IonizationEnergy.objects.create(ele=ele, energy=i)
            return JsonResponse({"code": 0, "msg": "add_success"})
        elif action == 'edit':
            if eid:
                Elements.objects.filter(pk=eid).update(symbol=symbol, atomic_number=atomic_number, relative_atomic_mass=relative_atomic_mass,
                                                       atomic_radius=atomic_radius, electronegativity=electronegativity, electronic_affinity=electronic_affinity,
                                                       introduction=introduction, extra=extra, cn_name=cn_name, color=color)
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
            ionizationenergy = '|'.join(ionizationenergy_list)
    return render(request, 'admin/ele_form.html', locals())


def hi_ele_list(request):
    list_name = '嗨元素'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        hi_element_list = HiElements.objects.all().values('id', 'ele__cn_name', 'introduction')
        count = hi_element_list.count()
        hi_element_list = hi_element_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(hi_element_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = HiElements.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/hi_ele_list.html', locals())


def hi_ele_mod(request, action):
    list_name = '嗨元素'
    post = request.POST
    hid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        hielementitems = post.get('hielementitems')
        introduction = post.get('introduction')
        hii_list = []
        if hielementitems:
            hii_list = hielementitems.split('|')
        if action == 'add':
            HiElements.objects.create(ele_id=ele_id, introduction=introduction)

        elif action == 'edit':
            if hid:
                ele = HiElements.objects.get(pk=hid)
                HiElementItems.objects.filter(ele_id=ele.ele_id).delete()
                HiElements.objects.filter(pk=hid).update(ele_id=ele_id, introduction=introduction)
        for i in hii_list:
            hi_list = re_find('(.*?) (.*?)', i, is_list=True)
            raise Exception
            HiElementItems.objects.create(ele_id=ele_id, content=hi_list[0], img=hi_list[1])

        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if hid:
            ele = HiElements.objects.get(pk=hid)
            hii_list = HiElementItems.objects.filter(ele_id=ele.ele_id)
            hielementitems_list = []
            for i in hii_list:
                hielementitems_list.append(i.content + ' 图片：' + i.img)
            hielementitems = '|'.join(hielementitems_list)
    elements_list = Elements.objects.all()
    return render(request, 'admin/hi_ele_form.html', locals())
