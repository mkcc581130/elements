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
from django.urls import path, re_path
import admin.views as admin_views
urlpatterns = [
    re_path('^$', admin_views.index, name='admin'),
    re_path('^upload_img/$', admin_views.upload_img, name='upload_img'),
    re_path('^login/$', admin_views.login_view, name='login'),
    re_path('^test/$', admin_views.test, name='test'),
    re_path('^update_p/$', admin_views.update_p, name='update_p'),
    re_path('^console/$', admin_views.console, name='console'),
    re_path('^ele_list/$', admin_views.ele_list, name='ele_list'),
    re_path('^ele_list/(edit|add)+/$', admin_views.ele_mod, name='ele_mod'),
    re_path('^hi_ele_list/$', admin_views.hi_ele_list, name='hi_ele_list'),
    re_path('^hi_ele_list/(edit|add)+/$', admin_views.hi_ele_mod, name='hi_ele_mod'),
    re_path('^ele_history_list/$', admin_views.ele_history_list, name='ele_history_list'),
    re_path('^ele_history_list/(edit|add)+/$', admin_views.ele_history_mod, name='ele_history_mod'),
    re_path('^ele_representative_list/$', admin_views.ele_representative_list, name='ele_representative_list'),
    re_path('^ele_representative_list/(edit|add)+/$', admin_views.ele_representative_mod, name='ele_representative_mod'),
    re_path('^ele_isotope_list/$', admin_views.ele_isotope_list, name='ele_isotope_list'),
    re_path('^ele_isotope_list/(edit|add)+/$', admin_views.ele_isotope_mod, name='ele_isotope_mod'),
    re_path('^ele_material_list/$', admin_views.ele_material_list, name='ele_material_list'),
    re_path('^ele_material_list/(edit|add)+/$', admin_views.ele_material_mod, name='ele_material_mod'),
    re_path('^ele_compound_list/$', admin_views.ele_compound_list, name='ele_compound_list'),
    re_path('^ele_compound_list/(edit|add)+/$', admin_views.ele_compound_mod, name='ele_compound_mod'),
    re_path('^ele_poem_list/$', admin_views.ele_poem_list, name='ele_poem_list'),
    re_path('^ele_poem_list/(edit|add)+/$', admin_views.ele_poem_mod, name='ele_poem_mod'),
    re_path('^ele_love_poem_list/$', admin_views.ele_love_poem_list, name='ele_love_poem_list'),
    re_path('^ele_love_poem_list/(edit|add)+/$', admin_views.ele_love_poem_mod, name='ele_love_poem_mod'),
    re_path('^ele_idiom_list/$', admin_views.ele_idiom_list, name='ele_idiom_list'),
    re_path('^ele_idiom_list/(edit|add)+/$', admin_views.ele_idiom_mod, name='ele_idiom_mod'),
    re_path('^ele_name_source_list/$', admin_views.ele_name_source_list, name='ele_name_source_list'),
    re_path('^ele_name_source_list/(edit|add)+/$', admin_views.ele_name_source_mod, name='ele_name_source_mod'),
    re_path('^ele_cartoon_list/$', admin_views.ele_cartoon_list, name='ele_cartoon_list'),
    re_path('^ele_cartoon_list/(edit|add)+/$', admin_views.ele_cartoon_mod, name='ele_cartoon_mod'),
    re_path('^ele_collection_list/$', admin_views.ele_collection_list, name='ele_collection_list'),
    re_path('^ele_collection_list/(edit|add)+/$', admin_views.ele_collection_mod, name='ele_collection_mod'),
    re_path('^ele_jingle_list/$', admin_views.ele_jingle_list, name='ele_jingle_list'),
    re_path('^ele_jingle_list/(edit|add)+/$', admin_views.ele_jingle_mod, name='ele_jingle_mod'),
    re_path('^ele_page_index_list/$', admin_views.ele_page_index_list, name='ele_page_index_list'),
    re_path('^ele_page_index_list/(edit|add)+/$', admin_views.ele_page_index_mod, name='ele_page_index_mod'),
    re_path('^ele_hi_theater_list/$', admin_views.ele_hi_theater_list, name='ele_hi_theater_list'),
    re_path('^ele_hi_theater_list/(edit|add)+/$', admin_views.ele_hi_theater_mod, name='ele_hi_theater_mod'),
]
