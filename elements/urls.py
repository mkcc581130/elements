"""elements URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
import main.views as main_views
urlpatterns = [
    re_path(r'^register/$', main_views.register, name='register'),
    re_path(r'^login/$', main_views.login, name='login'),
    re_path('^admin/', include('admin.urls')),
    re_path('^$', main_views.index, name='index'),
    re_path('^index/$', main_views.index, name='index1'),
    re_path('^comic/$', main_views.comic, name='comic'),
    re_path('^cartoon/$', main_views.cartoon, name='cartoon'),
    re_path('^family/$', main_views.family, name='family'),
    re_path('^painted/$', main_views.painted, name='painted'),
    re_path('^cartoon_img/$', main_views.cartoon_img, name='cartoon_img'),
    re_path('^poem/$', main_views.poem, name='poem'),
    re_path('^love_poem/$', main_views.love_poem, name='love_poem'),
    re_path('^jingle/$', main_views.jingle, name='jingle'),
    re_path('^structure/$', main_views.structure, name='structure'),
    re_path('^character/$', main_views.character, name='character'),
    re_path('^animation/$', main_views.animation, name='animation'),
    re_path('^collection/$', main_views.collection, name='collection'),
    re_path('^object/$', main_views.ele_object, name='object'),
    re_path('^name_source/$', main_views.name_source, name='name_source'),
    re_path('^idiom/$', main_views.idiom, name='idiom'),
    re_path('^hi/$', main_views.hi, name='hi'),
    re_path('^representative/$', main_views.representative, name='representative'),
    re_path('^ele_info/$', main_views.ele_info, name='ele_info'),
    re_path('^hi_ele/$', main_views.hi_ele, name='hi_ele'),
    re_path('^ele_history/$', main_views.ele_history, name='ele_history'),
    re_path('^ele_representative/$', main_views.ele_representative, name='ele_representative'),
    re_path('^ele_isotope/$', main_views.ele_isotope, name='ele_isotope'),
    re_path('^ele_material/$', main_views.ele_material, name='ele_material'),
    re_path('^ele_compound/$', main_views.ele_compound, name='ele_compound'),
    re_path('^ele_hi_comic/$', main_views.ele_hi_comic, name='ele_hi_comic'),
    re_path('^ele_hi_wallpaper/$', main_views.ele_hi_wallpaper, name='ele_hi_wallpaper'),
    re_path('^ele_periodic_img_(\d+)/$', main_views.ele_periodic_img, name='ele_periodic_img'),
    re_path('^get_love_poem_poster/(.*?).png$', main_views.get_love_poem_poster, name='get_love_poem_poster'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = main_views.page_forbidden

handler404 = main_views.page_not_found

handler500 = main_views.page_error
