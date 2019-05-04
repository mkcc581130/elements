from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
import pytz
import datetime
import os
import json
from django.contrib.auth.models import User
from .models import *
from .comm import visit_count, re_find
from .forms import RegistrationForm, LoginForm
from elements.settings import STATIC_ROOT
# Create your views here.
from PIL import Image, ImageFont, ImageDraw


def register(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            # 使用内置User自带create_user方法创建用户，不需要使用save()
            user = User.objects.create_user(username=username, password=password, email=email)

            # 如果直接使用objects.create()方法后不需要使用save()
            user_profile = UserProfile(user=user)
            user_profile.save()

            return HttpResponseRedirect("/login/")

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile', args=[user.id]))

            else:
                # 登陆失败
                return render(request, 'login.html', {'form': form, 'message': 'Wrong password. Please try again.'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def get_love_poem_poster(request, img_name):
    img_num = request.GET.get("img_num")
    poem_num = request.GET.get("poem_num")
    symbol = request.GET.get("symbol")
    top_img = Image.open(os.path.join(STATIC_ROOT, 'img/love_poem/love_poem_modal'+img_num+'.jpg'))
    (x, y) = top_img.size  # read image size
    x_s = 800  # define standard width
    y_s = y * x_s / x
    top_img = top_img.resize((x_s, int(y_s)), Image.ANTIALIAS)
    img = Image.new(top_img.mode, (800, 850), "#ffffff")
    img.paste(top_img, box=(0, 0))

    ttfont = ImageFont.truetype(os.path.join(STATIC_ROOT, 'font/baiqi.ttf'), 42)
    draw = ImageDraw.Draw(img)
    ele = ElementLovePoem.objects.get(ele__symbol=symbol)
    poem = ele.poem
    cn_name = ele.ele.cn_name
    poem_list = poem.split("|")
    po = poem_list[int(poem_num)]
    po_list = po.split('.')
    for p in range(len(po_list)):
        content = po_list[p]
        length = len(content)
        utf8_length = len(content.encode('utf-8'))  # 获取放入的文字编码后的长度
        length = (utf8_length - length) / 2 + length  # 汉字是2个字节 英文和数字是单字节
        an = (800 - length * 21) / 2
        draw.text((an, 530 + 75*p), content, fill=(57, 63, 68), font=ttfont)
    draw.text((690, 750), "--"+cn_name, fill=(57, 63, 68), font=ttfont)
    img.save(os.path.join(STATIC_ROOT, 'img/love_poem/poster.png'), quality=95)

    with open(os.path.join(STATIC_ROOT, 'img/love_poem/poster.png'), 'rb') as f:

        response = HttpResponse(f.read(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename='+img_name
        return response


def get_page(page_name):
    page_list = PageIndex.objects.all().order_by('index')
    pre_page = None
    next_page = None
    next_flag = 0
    for p in page_list:
        if next_flag:
            next_page = p
            break
        if p.en_name == page_name:
            next_flag = 1
        else:
            pre_page = p
    return {'page_list': page_list, 'pre_page': pre_page, 'next_page': next_page}


@visit_count
def index(request):
    page_name = 'index'
    page_info = get_page(page_name)
    return render(request, 'index.html', locals())


@visit_count
def comic(request):
    page_name = 'comic'
    page_name2 = 'comic'
    page_info = get_page(page_name)
    ei_list = ElementCartoon.objects.all().values('ele__symbol', 'ele__atomic_number', 'ele__cn_name', 'ele__across',
                                                  'ele__vertical', 'comic_introduction')
    left_nav = [['comic', '卡通元素周期表'], ['painted', '卡通手绘周期表'], ['cartoon_img', '卡通图片周期表'], ['cartoon', '卡通人物周期表'], ['hi', '嗨元素周期表'], ['family', '元素家族周期表']]
    return render(request, 'comic.html', locals())


@visit_count
def cartoon(request):
    page_name = 'comic'
    page_name2 = 'cartoon'
    page_info = get_page(page_name)
    ei_list = ElementCartoon.objects.all().values('ele__symbol', 'ele__atomic_number', 'ele__cn_name', 'ele__across', 'ele__vertical',
                                                  'cn_introduction')
    left_nav = [['comic', '卡通元素周期表'], ['painted', '卡通手绘周期表'], ['cartoon_img', '卡通图片周期表'], ['cartoon', '卡通人物周期表'], ['hi', '嗨元素周期表'], ['family', '元素家族周期表']]
    return render(request, 'cartoon.html', locals())


@visit_count
def family(request):
    page_name = 'comic'
    page_name2 = 'family'
    page_info = get_page(page_name)
    ei_list = ElementFamily.objects.all().values('ele__symbol', 'ele__atomic_number', 'ele__cn_name', 'ele__across', 'ele__vertical',
                                                 'feature', 'record', 'back_color')
    for e in ei_list:
        li = re_find('^(.*?) 形象：(.*?) 居所：(.*?) 出身：(.*?) 成员：(.*?)$', e['record'])
        if li:
            e.update({'character': li[0], 'figure': li[1], 'place': li[2], 'born': li[3], 'member': li[4]})

    left_nav = [['comic', '卡通元素周期表'], ['painted', '卡通手绘周期表'], ['cartoon_img', '卡通图片周期表'], ['cartoon', '卡通人物周期表'], ['hi', '嗨元素周期表'], ['family', '元素家族周期表']]
    return render(request, 'family.html', locals())


@visit_count
def painted(request):
    page_name = 'comic'
    page_name2 = 'painted'
    page_info = get_page(page_name)
    ei_list = ElementCartoon.objects.all().values('ele__symbol', 'ele__atomic_number', 'ele__cn_name', 'ele__across', 'ele__vertical',
                                                  'painted_introduction')
    left_nav = [['comic', '卡通元素周期表'], ['painted', '卡通手绘周期表'], ['cartoon_img', '卡通图片周期表'], ['cartoon', '卡通人物周期表'], ['hi', '嗨元素周期表'], ['family', '元素家族周期表']]
    return render(request, 'painted.html', locals())


@visit_count
def cartoon_img(request):
    page_name = 'comic'
    page_name2 = 'cartoon_img'
    page_info = get_page(page_name)
    ei_list = ElementCartoon.objects.all().values('ele__symbol', 'ele__atomic_number', 'ele__cn_name', 'ele__across', 'ele__vertical',
                                                  'img_introduction')
    left_nav = [['comic', '卡通元素周期表'], ['painted', '卡通手绘周期表'], ['cartoon_img', '卡通图片周期表'], ['cartoon', '卡通人物周期表'], ['hi', '嗨元素周期表'], ['family', '元素家族周期表']]
    return render(request, 'cartoon_img.html', locals())


@visit_count
def collection(request):
    page_name = 'object'
    page_name2 = 'collection'
    page_info = get_page(page_name)
    ei_list = ElementCollection.objects.all().values('ele__symbol', 'ele__atomic_number', 'ele__across', 'ele__vertical',
                                                     'introduction')
    left_nav = [['object', '单质收藏周期表（冥灵版）'], ['collection', '单质收藏周期表（爱好者）'], ['animation', '单质收藏周期表（收藏家）']]
    return render(request, 'collection.html', locals())


@visit_count
def animation(request):
    page_name = 'object'
    page_name2 = 'animation'
    page_info = get_page(page_name)
    left_nav = [['object', '单质收藏周期表（冥灵版）'], ['collection', '单质收藏周期表（爱好者）'], ['animation', '单质收藏周期表（收藏家）']]
    return render(request, 'animation.html', locals())


@visit_count
def ele_object(request):
    page_name = 'object'
    page_name2 = 'object'
    page_info = get_page(page_name)
    ei_list = ElementObject.objects.all().values('ele__symbol', 'ele__atomic_number', 'ele__across', 'ele__vertical',
                                                 'number')
    left_nav = [['object', '单质收藏周期表（冥灵版）'], ['collection', '单质收藏周期表（爱好者）'], ['animation', '单质收藏周期表（收藏家）']]
    return render(request, 'object.html', locals())


@visit_count
def hi(request):
    page_name = 'comic'
    page_name2 = 'hi'
    page_info = get_page(page_name)
    ei_list = Elements.objects.all().values('symbol', 'atomic_number', 'across', 'vertical')
    left_nav = [['comic', '卡通元素周期表'], ['painted', '卡通手绘周期表'], ['cartoon_img', '卡通图片周期表'], ['cartoon', '卡通人物周期表'], ['hi', '嗨元素周期表'], ['family', '元素家族周期表']]
    return render(request, 'hi.html', locals())


@visit_count
def representative(request):
    page_name = 'representative'
    page_info = get_page(page_name)
    ei_list = Elements.objects.all().values('symbol', 'atomic_number', 'across', 'vertical')
    return render(request, 'representative.html', locals())


@visit_count
def jingle(request):
    page_name = 'jingle'
    page_info = get_page(page_name)
    ei_list = ElementJingle.objects.all().values('ele__symbol', 'ele__atomic_number',
                                                 'ele__across', 'ele__vertical', 'jingle')
    return render(request, 'jingle.html', locals())


@visit_count
def name_source(request):
    page_name = 'name_source'
    page_info = get_page(page_name)
    ei_list = ElementNameSource.objects.all().values('ele__symbol', 'ele__atomic_number', 'ele__relative_atomic_mass',
                                                     'ele__cn_name', 'ele__pinyin', 'ele__en_name',
                                                     'ele__across', 'ele__vertical', 'category', 'introduction')
    return render(request, 'name_source.html', locals())


@visit_count
def structure(request):
    page_name = 'structure'
    page_info = get_page(page_name)
    ei_list = Elements.objects.all().values('symbol', 'atomic_number', 'relative_atomic_mass', 'element_type',
                                            'outer_electron', 'electron_configuration', 'cn_name', 'en_name', 'across',
                                            'vertical')
    return render(request, 'structure.html', locals())


@visit_count
def character(request):
    page_name = 'character'
    # page_info = get_page(page_name)
    ei_list = Elements.objects.all().order_by('atomic_number').values('symbol', 'atomic_number', 'cn_name', 'en_name', 'across',
                                            'vertical', 'electronegativity', 'atomic_radius',
                                            'electronic_affinity')
    ran = range(1, 119)
    return render(request, 'character.html', locals())


@visit_count
def idiom(request):
    page_name = 'idiom'
    page_info = get_page(page_name)
    ei_list = ElementIdiom.objects.all().values('ele__symbol', 'ele__atomic_number', 'ele__across', 'ele__vertical',
                                               'idiom', 'pre_idiom', 'introduction')
    return render(request, 'idiom.html', locals())


@visit_count
def poem(request):
    page_name = 'poem'
    page_info = get_page(page_name)
    ep_list = ElementPoem.objects.all().values('ele__symbol', 'ele__cn_name', 'ele__en_name', 'ele__atomic_number',
                                               'ele__across', 'ele__vertical', 'poem', 'en_poem')
    return render(request, 'poem.html', locals())


@visit_count
def love_poem(request):
    page_name = 'love_poem'
    page_info = get_page(page_name)
    ep_list = ElementLovePoem.objects.all().values('ele__symbol', 'ele__cn_name', 'ele__en_name', 'ele__atomic_number',
                                               'ele__across', 'ele__vertical', 'poem')
    return render(request, 'love_poem.html', locals())


@visit_count
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


@visit_count
def hi_ele(request):
    symbol = request.GET.get("symbol")
    hiele = HiElements.objects.get(ele__symbol=symbol)
    next_ele = Elements.objects.filter(atomic_number=hiele.ele.atomic_number + 1)
    pre_ele = Elements.objects.filter(atomic_number=hiele.ele.atomic_number - 1)
    hiele_item = HiElementItems.objects.filter(ele_id=hiele.ele_id)
    return render(request, 'element/hi_ele.html', locals())


@visit_count
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


@visit_count
def ele_representative(request):
    symbol = request.GET.get("symbol")
    try:
        ele = Elements.objects.get(symbol=symbol)
        ere = ElementRepresentative.objects.get(ele_id=ele.id)
    except ElementRepresentative.DoesNotExist:
        return page_forbidden(request)
    item_list = ElementRepresentativeItem.objects.filter(representative_id=ere.id)
    duty_list = ere.duty.split("|")
    symbol = request.GET.get("symbol")
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


@visit_count
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


@visit_count
def ele_material(request):
    symbol = request.GET.get("symbol")
    ele = Elements.objects.get(symbol=symbol)
    eme = ElementMaterial.objects.get(ele_id=ele.id, is_compound=False)
    eme_list = ElementMaterial.objects.filter(ele_id=ele.id)
    eme_length = len(eme_list)
    pre_allotrope_list = eme.allotrope.split('|')
    allotrope_list = []
    pre_application_list = eme.application.split('|')
    application_list = []
    experiment_video_list = eme.experiment_video.split('|')
    experiment_list = []
    if eme.experiment_video:
        video_list = eme.experiment_video.split(",")
    for p in pre_allotrope_list:
        if p:
            li = re_find('^(.*?) 介绍：(.*?) 图片：(.*?) 视频：(.*?)$', p)
            allotrope_list.append([li[0], li[1], li[2], li[3]])
    for p in pre_application_list:
        if p:
            li = re_find('^(.*?) 图片：(.*?) 视频：(.*?)$', p)
            application_list.append([li[0], li[1], li[2]])
    for p in experiment_video_list:
        if p:
            li = re_find('^(.*?) 介绍：(.*?)$', p)
            experiment_list.append([li[0], li[1]])

    next_ele = Elements.objects.filter(atomic_number=ele.atomic_number + 1)
    pre_ele = Elements.objects.filter(atomic_number=ele.atomic_number - 1)
    return render(request, 'element/ele_material.html', locals())


@visit_count
def ele_compound(request):
    symbol = request.GET.get("symbol")
    compound_id = request.GET.get("cid")
    ele = Elements.objects.get(symbol=symbol)
    em = ElementMaterial.objects.filter(ele_id=ele.id, is_compound=True)
    eme_list = ElementMaterial.objects.filter(ele_id=ele.id)
    eme_length = len(eme_list)
    if not compound_id:
        eme = em[0]
    else:
        eme = em.filter(pk=compound_id)[0]
    pre_allotrope_list = eme.allotrope.split('|')
    allotrope_list = []
    pre_application_list = eme.application.split('|')
    application_list = []
    experiment_video_list = eme.experiment_video.split('|')
    experiment_list = []
    if eme.experiment_video:
        video_list = eme.experiment_video.split(",")
    for p in pre_allotrope_list:
        if p:
            li = re_find('^(.*?) 介绍：(.*?) 图片：(.*?) 视频：(.*?)$', p)
            allotrope_list.append([li[0], li[1], li[2], li[3]])
    for p in pre_application_list:
        if p:
            li = re_find('^(.*?) 图片：(.*?) 视频：(.*?)$', p)
            application_list.append([li[0], li[1], li[2]])
    for p in experiment_video_list:
        if p:
            li = re_find('^(.*?) 介绍：(.*?)$', p)
            experiment_list.append([li[0], li[1]])

    next_ele = Elements.objects.filter(atomic_number=ele.atomic_number + 1)
    pre_ele = Elements.objects.filter(atomic_number=ele.atomic_number - 1)
    return render(request, 'element/ele_compound.html', locals())


@visit_count
def ele_hi_comic(request):
    type = request.GET.get("type", "1")
    hua = request.GET.get("hua")
    if type == '1':
        if not hua:
            hua = "001"
        hi_comic = HiTheater.objects.get(type=type, hua=hua)
    elif type == '2':
        if not hua:
            hua = "000_1"
        elif len(hua) == 3:
            hua += "_1"
        hi_comic = HiTheater.objects.get(type=type, hua=hua)
    comic_list = HiTheater.objects.filter(type=type)
    return render(request, 'element/ele_hi_comic.html', locals())


@visit_count
def ele_hi_wallpaper(request):
    page = request.GET.get("page")
    if not page:
        wallpaper_list = HiWallpaper.objects.all().order_by('sort')[:8]
    else:
        page = int(page)
        wallpaper_list = HiWallpaper.objects.all().order_by('sort')[page*4:page*4+4].values('file_name')
        return HttpResponse(json.dumps({"list": list(wallpaper_list)}))
    return render(request, 'element/ele_hi_wallpaper.html', locals())


@visit_count
def ele_periodic_img(request, ptype):
    page = request.GET.get("page")
    page_name = "ele_periodic_img_"+str(ptype)
    if ptype == "1":
        wallpaper_list = PeriodicImg.objects.filter(type=1)
    elif ptype == "2":
        wallpaper_list = PeriodicImg.objects.filter(type=2)
    if not page:
        wallpaper_list = wallpaper_list.order_by('sort')[:8]
    else:
        page = int(page)
        periodic_img_list = wallpaper_list.order_by('sort')[page*4:page*4+4].values('file_name')
        return HttpResponse(json.dumps({"list": list(periodic_img_list)}))
    page_info = get_page(page_name)
    return render(request, 'periodic_img.html', locals())


def page_not_found(request, **kwargs):
    error_code = 404
    error_info = '未找到相应页面，请确认后重试！'
    response = render(request, 'error.html', locals())
    response.status_code = error_code
    return response


def page_error(request, **kwargs):
    error_code = 500
    error_info = '服务器错误，等待程序猿ing'
    response = render(request, 'error.html', locals())
    response.status_code = error_code
    return response


def page_forbidden(request, **kwargs):
    error_code = 403
    error_info = '此页面尚未完善，无法访问哦，点击返回'
    response = render(request, 'error.html', locals())
    response.status_code = error_code
    return response
