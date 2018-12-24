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
    re_path('^login/$', admin_views.login_view, name='login'),
    re_path('^console/$', admin_views.console, name='console'),
    re_path('^ele_list/$', admin_views.ele_list, name='ele_list'),
    re_path('^ele_list/(edit|add)+/$', admin_views.ele_mod, name='ele_mod'),
]