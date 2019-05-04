import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.contrib.auth.decorators import login_required

from main.models import *
from main.comm import re_find
from django.views.decorators.csrf import csrf_exempt


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

def update_p(request):
    his_list = ElementHistory.objects.all()
    for h in his_list:
        h.introduction = '<p>' + h.introduction.replace('<br>', '</p><p>') + '</p>'
        h.save()
    return HttpResponse('OK')

def ele_list(request):
    list_name = '元素'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = Elements.objects.all().order_by('atomic_number').values('atomic_number', 'cn_name', 'symbol', 'id')
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
        symbol = post.get('symbol', "")
        atomic_number = post.get('atomic_number', "")
        relative_atomic_mass = post.get('relative_atomic_mass', "")
        atomic_radius_type = post.get('atomic_radius_type', "1")
        element_type = post.get('element_type', "1")
        atomic_radius = post.get('atomic_radius', "")
        electronegativity = post.get('electronegativity', "")
        electronic_affinity = post.get('electronic_affinity', "")
        introduction = post.get('introduction', "")
        ionizationenergy = post.get('ionizationenergy', "")
        electron_configuration = post.get('electron_configuration', "")
        color = post.get('color', "")
        ie_list = []
        if ionizationenergy:
            ie_list = ionizationenergy.split('|')
        extra = post.get('extra', "")
        relate_video = post.get('relate_video', "")
        relate_video_name = post.get('relate_video_name', "")
        cn_name = post.get('cn_name', "")
        en_name = post.get('en_name', "")
        pinyin = post.get('pinyin', "")

        outer_electron = post.get('outer_electron', "")
        if not atomic_radius_type:
            atomic_radius_type = '1'
        if action == 'add':
            ele = Elements.objects.create(symbol=symbol, atomic_number=atomic_number,
                                          relative_atomic_mass=relative_atomic_mass, atomic_radius=atomic_radius,
                                          atomic_radius_type=atomic_radius_type, electronegativity=electronegativity,
                                          electronic_affinity=electronic_affinity, introduction=introduction,
                                          extra=extra, cn_name=cn_name, outer_electron=outer_electron, color=color,
                                          en_name=en_name, pinyin=pinyin, electron_configuration=electron_configuration,
                                          element_type=element_type, relate_video=relate_video, relate_video_name=relate_video_name)
            for i in ie_list:
                IonizationEnergy.objects.create(ele=ele, energy=i)
            return JsonResponse({"code": 0, "msg": "add_success"})
        elif action == 'edit':
            if eid:
                Elements.objects.filter(pk=eid).update(symbol=symbol, atomic_number=atomic_number,
                                                       relative_atomic_mass=relative_atomic_mass,
                                                       atomic_radius=atomic_radius,
                                                       atomic_radius_type=atomic_radius_type,
                                                       electronegativity=electronegativity,
                                                       electronic_affinity=electronic_affinity,
                                                       introduction=introduction, extra=extra, cn_name=cn_name,
                                                       outer_electron=outer_electron, color=color, en_name=en_name,
                                                       pinyin=pinyin, electron_configuration=electron_configuration,
                                                       element_type=element_type, relate_video=relate_video, relate_video_name=relate_video_name)
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
        hi_element_list = HiElements.objects.all().values('id', 'ele__atomic_number', 'ele__cn_name', 'introduction')
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
    if hid:
        ele = HiElements.objects.get(pk=hid)
    if post:
        ele_id = post.get('ele_id')
        hielementitems = post.get('hielementitems')
        introduction = post.get('introduction')
        light_color = post.get('light_color')
        dark_color = post.get('dark_color')
        hii_list = []
        if hielementitems:
            hii_list = hielementitems.split('|')
        if action == 'add':
            HiElements.objects.create(ele_id=ele_id, introduction=introduction, dark_color=dark_color, light_color=light_color)

        elif action == 'edit':
            if hid:
                HiElementItems.objects.filter(ele_id=ele.ele_id).delete()
                HiElements.objects.filter(pk=hid).update(ele_id=ele_id, introduction=introduction, dark_color=dark_color, light_color=light_color)
        for i in hii_list:
            hi_list = re_find('^(.*?) 图片：(.*?)$', i)
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
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/hi_ele_form.html', locals())


def ele_history_list(request):
    list_name = '元素发现史'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = Elements.objects.all().values('id').annotate(count=Count('elementhistory')).values('id', 'atomic_number', 'cn_name', 'count')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementHistory.objects.filter(ele_id=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_history_list.html', locals())


def ele_history_mod(request, action):
    list_name = '元素发现史'
    post = request.POST
    eid = request.GET.get("id")
    if post:
        elementhistory = post.get('elementhistory')
        ehi_list = []
        if elementhistory:
            ehi_list = elementhistory.split('|')
        if action == 'edit':
            if eid:
                ElementHistory.objects.filter(ele_id=eid).delete()
            for i in ehi_list:
                eh_list = re_find('^(.*?) 年份：(.*?) 科学家：(.*?) 图片：(.*?) 排序：(.*?)$', i)
                ElementHistory.objects.create(ele_id=eid, introduction=eh_list[0], year=eh_list[1], scientist=eh_list[2]
                                              , img=eh_list[3], sort=eh_list[4])

        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if eid:
            ehi_list = ElementHistory.objects.filter(ele_id=eid)
            elementhistory_list = []
            for i in ehi_list:
                img = i.img if i.img else ''
                elementhistory_list.append(i.introduction + ' 年份：' + str(i.year) + ' 科学家：' + i.scientist + ' 图片：'
                                           + img + ' 排序：' + str(i.sort))
            elementhistory = '|'.join(elementhistory_list)
    return render(request, 'admin/ele_history_form.html', locals())


def ele_representative_list(request):
    list_name = '元素代言人'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementRepresentative.objects.all().values('id', 'ele__cn_name', 'pro_name', 'country')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementRepresentative.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_representative_list.html', locals())


def ele_representative_mod(request, action):
    list_name = '元素代言人'
    post = request.POST
    rid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        pro_name = post.get('pro_name')
        university = post.get('university')
        country = post.get('country')
        duty = post.get('duty')
        top_color = post.get('top_color')
        main_color = post.get('main_color')
        title_list = post.getlist('title')
        img_info_list = post.getlist('img_info')
        img_type_list = post.getlist('img_type')
        introduction_list = post.getlist('introduction')
        list_len = len(title_list)
        if action == 'add':
            er = ElementRepresentative.objects.create(ele_id=ele_id, duty=duty, pro_name=pro_name, university=university
                                                      , country=country, main_color=main_color, top_color=top_color)
            for i in range(list_len):
                ElementRepresentativeItem.objects.create(representative_id=er.id, title=title_list[i],
                                                         img_info=img_info_list[i], img_type=img_type_list[i],
                                                         introduction=introduction_list[i])
        elif action == 'edit':
            if rid:
                er = ElementRepresentative.objects.filter(pk=rid).update(ele_id=ele_id, duty=duty, pro_name=pro_name
                                                                         , university=university, country=country,
                                                                         main_color=main_color, top_color=top_color)
                ElementRepresentativeItem.objects.filter(representative_id=rid).delete()
                for i in range(list_len):
                    ElementRepresentativeItem.objects.create(representative_id=rid, title=title_list[i],
                                                             img_info=img_info_list[i], img_type=img_type_list[i],
                                                             introduction=introduction_list[i])
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if rid:
            ere = ElementRepresentative.objects.get(id=rid)
            item_list = ElementRepresentativeItem.objects.filter(representative_id=rid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_representative_form.html', locals())


def ele_isotope_list(request):
    list_name = '元素代言人'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementIsotope.objects.all().values('id', 'ele__symbol', 'guide')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementIsotope.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_isotope_list.html', locals())


def ele_isotope_mod(request, action):
    list_name = '同位素'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        stable_isotope = post.get('stable_isotope')
        guide = post.get('guide')
        introduction = post.get('introduction')
        if action == 'add':
            ElementIsotope.objects.create(ele_id=ele_id, stable_isotope=stable_isotope, guide=guide,
                                          introduction=introduction)
        elif action == 'edit':
            if iid:
                er = ElementIsotope.objects.filter(pk=iid).update(ele_id=ele_id, stable_isotope=stable_isotope,
                                                                  guide=guide, introduction=introduction)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eie = ElementIsotope.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_isotope_form.html', locals())


def ele_material_list(request):
    list_name = '元素单质'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementMaterial.objects.filter(is_compound=False).values('id', 'ele__symbol', 'introduction')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementMaterial.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_material_list.html', locals())


def ele_material_mod(request, action):
    list_name = '元素单质'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        other_name = post.get('other_name', "")
        other_en_name = post.get('other_en_name', "")
        introduction = post.get('introduction', "")
        has_allotrope = post.get('has_allotrope', "")
        allotrope = post.get('allotrope', "")
        application = post.get('application', "")
        experiment_video = post.get('experiment_video', "")
        melting_point = post.get('melting_point', "")
        boiling_point = post.get('boiling_point', "")
        density = post.get('density', "")
        caloric = post.get('caloric', "")
        chemical_formula = post.get('chemical_formula', "")
        relative_molecular_mass = post.get('relative_molecular_mass', "")
        structure_img = post.get('structure_img', "")
        if action == 'add':
            ElementMaterial.objects.create(ele_id=ele_id, other_name=other_name, other_en_name=other_en_name,
                                           allotrope=allotrope, has_allotrope=has_allotrope, application=application,
                                           introduction=introduction, experiment_video=experiment_video,
                                           melting_point=melting_point, boiling_point=boiling_point, structure_img=structure_img,
                                           density=density, caloric=caloric, relative_molecular_mass=relative_molecular_mass,chemical_formula=chemical_formula)
        elif action == 'edit':
            if iid:
                er = ElementMaterial.objects.filter(pk=iid).update(ele_id=ele_id, other_name=other_name,
                                                                   other_en_name=other_en_name, allotrope=allotrope,
                                                                   has_allotrope=has_allotrope,
                                                                   application=application, introduction=introduction,
                                                                   experiment_video=experiment_video, structure_img=structure_img,
                                                                   melting_point=melting_point, boiling_point=boiling_point,
                                                                   density=density, caloric=caloric,
                                                                   relative_molecular_mass=relative_molecular_mass,
                                                                   chemical_formula=chemical_formula)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eme = ElementMaterial.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_material_form.html', locals())


def ele_compound_list(request):
    list_name = '元素单质'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementMaterial.objects.filter(is_compound=True).values('id', 'ele__symbol', 'chemical_formula', 'introduction')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementMaterial.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_compound_list.html', locals())


def ele_compound_mod(request, action):
    list_name = '元素单质'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        other_name = post.get('other_name', "")
        other_en_name = post.get('other_en_name', "")
        introduction = post.get('introduction', "")
        has_allotrope = post.get('has_allotrope', "")
        allotrope = post.get('allotrope', "")
        application = post.get('application', "")
        experiment_video = post.get('experiment_video', "")
        melting_point = post.get('melting_point', "")
        boiling_point = post.get('boiling_point', "")
        density = post.get('density', "")
        caloric = post.get('caloric', "")
        chemical_formula = post.get('chemical_formula', "")
        relative_molecular_mass = post.get('relative_molecular_mass', "")
        compound = post.get('compound', "")
        structure_img = post.get('structure_img', "")
        if action == 'add':
            ElementMaterial.objects.create(ele_id=ele_id, other_name=other_name, other_en_name=other_en_name,
                                           allotrope=allotrope, has_allotrope=has_allotrope, application=application,
                                           introduction=introduction, experiment_video=experiment_video,
                                           melting_point=melting_point, boiling_point=boiling_point,
                                           density=density, caloric=caloric, is_compound=True,compound=compound,
                                           relative_molecular_mass=relative_molecular_mass,structure_img=structure_img,
                                           chemical_formula=chemical_formula)
        elif action == 'edit':
            if iid:
                er = ElementMaterial.objects.filter(pk=iid).update(ele_id=ele_id, other_name=other_name,
                                                                   other_en_name=other_en_name, allotrope=allotrope,
                                                                   has_allotrope=has_allotrope,
                                                                   application=application, introduction=introduction,
                                                                   experiment_video=experiment_video,compound=compound,
                                                                   melting_point=melting_point, boiling_point=boiling_point,
                                                                   density=density, caloric=caloric,structure_img=structure_img,
                                                                   relative_molecular_mass=relative_molecular_mass,chemical_formula=chemical_formula)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eme = ElementMaterial.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_compound_form.html', locals())


def ele_poem_list(request):
    list_name = '三行诗'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementPoem.objects.all().values('id', 'ele__symbol', 'poem', 'en_poem')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementPoem.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_poem_list.html', locals())


def ele_poem_mod(request, action):
    list_name = '三行诗'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        poem = post.get('poem')
        en_poem = post.get('en_poem')
        if action == 'add':
            ElementPoem.objects.create(ele_id=ele_id, poem=poem, en_poem=en_poem)
        elif action == 'edit':
            if iid:
                er = ElementPoem.objects.filter(pk=iid).update(ele_id=ele_id, poem=poem, en_poem=en_poem)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eme = ElementPoem.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_poem_form.html', locals())


def ele_love_poem_list(request):
    list_name = '情诗'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementLovePoem.objects.all().values('id', 'ele__symbol', 'poem')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementLovePoem.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_love_poem_list.html', locals())


def ele_love_poem_mod(request, action):
    list_name = '情诗'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        poem = post.get('poem')
        if action == 'add':
            ElementLovePoem.objects.create(ele_id=ele_id, poem=poem)
        elif action == 'edit':
            if iid:
                er = ElementLovePoem.objects.filter(pk=iid).update(ele_id=ele_id, poem=poem)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eme = ElementLovePoem.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_love_poem_form.html', locals())


def ele_idiom_list(request):
    list_name = '成语'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementIdiom.objects.all().values('id', 'ele__symbol', 'idiom', 'pre_idiom')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementIdiom.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_idiom_list.html', locals())


def ele_idiom_mod(request, action):
    list_name = '成语'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        idiom = post.get('idiom')
        pre_idiom = post.get('pre_idiom')
        introduction = post.get('introduction')
        if action == 'add':
            ElementIdiom.objects.create(ele_id=ele_id, idiom=idiom, pre_idiom=pre_idiom, introduction=introduction)
        elif action == 'edit':
            if iid:
                er = ElementIdiom.objects.filter(pk=iid).update(ele_id=ele_id, idiom=idiom, pre_idiom=pre_idiom, introduction=introduction)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eie = ElementIdiom.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_idiom_form.html', locals())


def ele_name_source_list(request):
    list_name = '命名来源'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementNameSource.objects.all().values('id', 'ele__symbol', 'introduction')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementNameSource.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_name_source_list.html', locals())


def ele_name_source_mod(request, action):
    list_name = '命名来源'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        category = post.get('category')
        introduction = post.get('introduction')
        if action == 'add':
            ElementNameSource.objects.create(ele_id=ele_id, category=category, introduction=introduction)
        elif action == 'edit':
            if iid:
                er = ElementNameSource.objects.filter(pk=iid).update(ele_id=ele_id, category=category,
                                                                     introduction=introduction)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eie = ElementNameSource.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_name_source_form.html', locals())


def ele_cartoon_list(request):
    list_name = '卡通'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementCartoon.objects.all().values('id', 'ele__symbol', 'cn_introduction')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementCartoon.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_cartoon_list.html', locals())


def ele_cartoon_mod(request, action):
    list_name = '卡通'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        cn_introduction = post.get('cn_introduction')
        comic_introduction = post.get('comic_introduction')
        painted_introduction = post.get('painted_introduction')
        img_introduction = post.get('img_introduction')
        if action == 'add':
            ElementCartoon.objects.create(ele_id=ele_id, cn_introduction=cn_introduction,
                                          comic_introduction=comic_introduction,
                                          painted_introduction=painted_introduction,
                                          img_introduction=img_introduction)
        elif action == 'edit':
            if iid:
                er = ElementCartoon.objects.filter(pk=iid).update(ele_id=ele_id, cn_introduction=cn_introduction,
                                                                  comic_introduction=comic_introduction,
                                                                  painted_introduction=painted_introduction,
                                                                  img_introduction=img_introduction)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eie = ElementCartoon.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_cartoon_form.html', locals())


def ele_collection_list(request):
    list_name = '收藏'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementCollection.objects.all().values('id', 'ele__symbol', 'introduction')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementCollection.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_collection_list.html', locals())


def ele_collection_mod(request, action):
    list_name = '收藏'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        introduction = post.get('introduction')
        if action == 'add':
            ElementCollection.objects.create(ele_id=ele_id, introduction=introduction)
        elif action == 'edit':
            if iid:
                er = ElementCollection.objects.filter(pk=iid).update(ele_id=ele_id, introduction=introduction)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eie = ElementCollection.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_collection_form.html', locals())


def ele_object_list(request):
    list_name = '实物'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementObject.objects.all().values('id', 'ele__symbol', 'number')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementObject.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_object_list.html', locals())


def ele_object_mod(request, action):
    list_name = '实物'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        number = post.get('number')
        if action == 'add':
            ElementObject.objects.create(ele_id=ele_id, number=number)
        elif action == 'edit':
            if iid:
                er = ElementObject.objects.filter(pk=iid).update(ele_id=ele_id, number=number)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eie = ElementObject.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_object_form.html', locals())


def ele_jingle_list(request):
    list_name = '顺口溜'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementJingle.objects.all().values('id', 'ele__symbol', 'jingle')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementJingle.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_jingle_list.html', locals())


def ele_jingle_mod(request, action):
    list_name = '顺口溜'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        jingle = post.get('jingle')
        if action == 'add':
            ElementJingle.objects.create(ele_id=ele_id, jingle=jingle)
        elif action == 'edit':
            if iid:
                er = ElementJingle.objects.filter(pk=iid).update(ele_id=ele_id, jingle=jingle)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eie = ElementJingle.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_jingle_form.html', locals())


def ele_family_list(request):
    list_name = '元素家族'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = ElementFamily.objects.all().values('id', 'ele__symbol', 'feature')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = ElementFamily.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_family_list.html', locals())


def ele_family_mod(request, action):
    list_name = '元素家族'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        feature = post.get('feature')
        record = post.get('record')
        back_color = post.get('back_color')
        if action == 'add':
            ElementFamily.objects.create(ele_id=ele_id, feature=feature, record=record, back_color=back_color)
        elif action == 'edit':
            if iid:
                er = ElementFamily.objects.filter(pk=iid).update(ele_id=ele_id, feature=feature, record=record, back_color=back_color)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            eie = ElementFamily.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_family_form.html', locals())


def ele_page_index_list(request):
    list_name = '周期表排序'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = PageIndex.objects.all().values('id', 'cn_name', 'en_name', 'index')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = PageIndex.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_page_index_list.html', locals())


def ele_page_index_mod(request, action):
    list_name = '周期表排序'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        page_index = post.get('index')
        cn_name = post.get('cn_name')
        en_name = post.get('en_name')
        if action == 'add':
            PageIndex.objects.create(index=page_index, cn_name=cn_name, en_name=en_name)
        elif action == 'edit':
            if iid:
                er = PageIndex.objects.filter(pk=iid).update(index=page_index, cn_name=cn_name, en_name=en_name)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            ele = PageIndex.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_page_index_form.html', locals())


def ele_hi_theater_list(request):
    list_name = '嗨元素长漫画'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    type = request.GET.get('type')
    if page and limit:
        page = int(page)
        limit = int(limit)
        query_dict = {}
        elements_list = HiTheater.objects.all()
        if type:
            query_dict['type'] = type
        elements_list = elements_list.filter(**query_dict).values('id', 'type', 'hua', 'title')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = HiTheater.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_hi_theater_list.html', locals())


def ele_hi_theater_mod(request, action):
    list_name = '嗨元素长漫画'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        ele_id = post.get('ele_id')
        hua = post.get('hua')
        title = post.get('title')
        type = post.get('type')
        introduction = post.get('introduction')
        if action == 'add':
            HiTheater.objects.create(hua=hua, title=title, type=type, introduction=introduction)
        elif action == 'edit':
            if iid:
                HiTheater.objects.filter(pk=iid).update(hua=hua, title=title, type=type, introduction=introduction)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            ele = HiTheater.objects.get(id=iid)
    elements_list = Elements.objects.all().order_by('atomic_number')
    return render(request, 'admin/ele_hi_theater_form.html', locals())


def ele_hi_wallpaper_list(request):
    list_name = '嗨元素壁纸'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = HiWallpaper.objects.all().values('id', 'file_name', 'sort')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = HiWallpaper.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_hi_wallpaper_list.html', locals())


def ele_hi_wallpaper_mod(request, action):
    list_name = '嗨元素壁纸'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        file_name = post.get('file_name')
        sort = post.get('sort')
        if action == 'add':
            HiWallpaper.objects.create(file_name=file_name, sort=sort)
        elif action == 'edit':
            if iid:
                HiWallpaper.objects.filter(pk=iid).update(file_name=file_name, sort=sort)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            ele = HiWallpaper.objects.get(id=iid)
    return render(request, 'admin/ele_hi_wallpaper_form.html', locals())


def ele_periodic_img_list(request):
    list_name = '周期表图片'
    page = request.GET.get('page')
    limit = request.GET.get('limit')
    if page and limit:
        page = int(page)
        limit = int(limit)
        elements_list = PeriodicImg.objects.all().values('id', 'file_name', 'type', 'sort')
        count = elements_list.count()
        elements_list = elements_list[limit * (page - 1): limit * page]
        return JsonResponse({"code": 0, "msg": "", "count": count, "data": list(elements_list)})
    # 删除操作
    del_data = request.GET.getlist('del_data[]')
    if del_data:
        for i in del_data:
            e = PeriodicImg.objects.filter(pk=i)
            if e:
                e.delete()
        return JsonResponse({"code": 0, "msg": "del_success"})
    return render(request, 'admin/ele_periodic_img_list.html', locals())


def ele_periodic_img_mod(request, action):
    list_name = '周期表图片'
    post = request.POST
    iid = request.GET.get("id")
    if post:
        file_name = post.get('file_name')
        sort = post.get('sort')
        type = post.get('type')
        if action == 'add':
            PeriodicImg.objects.create(file_name=file_name, type=type, sort=sort)
        elif action == 'edit':
            if iid:
                PeriodicImg.objects.filter(pk=iid).update(file_name=file_name, type=type, sort=sort)
        return JsonResponse({"code": 0, "msg": action + "_success"})
    if action == 'edit':
        if iid:
            ele = PeriodicImg.objects.get(id=iid)
    return render(request, 'admin/ele_periodic_img_form.html', locals())


@csrf_exempt
def upload_img(request):
    source = request.GET.get("source")
    new_img = IMG(img=request.FILES.get('file'), name=request.FILES.get('file').name, source=source)
    new_img.save()
    return HttpResponse(json.dumps({"errno": 0, "data": [new_img.img.url]}))


def test(request):
    return render(request, 'admin/test.html', locals())
