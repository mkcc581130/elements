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
    re_path('^admin/', include('admin.urls')),
    re_path('^$', main_views.index, name='index'),
    re_path('^ele_info/$', main_views.ele_info, name='ele_info'),
    re_path('^hi_ele/$', main_views.hi_ele, name='hi_ele'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
