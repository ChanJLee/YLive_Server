"""ylive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from ylive.admin import init_category, init_user, init_anchor, init_follow, foo
from ylive.view import login, register, logout, open_broadcast

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/login/$', login),
    url(r'^user/register/$', register),
    url(r'^user/logout/$', logout),
    url(r'^admin/init/category/$', init_category),
    url(r'^admin/init/user/$', init_user),
    url(r'^admin/init/anchor/$', init_anchor),
    url(r'^admin/init/follow/$', init_follow),
    url(r'^foo/$', foo),
    url(r'^anchor/broadcast/open/$', open_broadcast)
]
