# coding=utf-8
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

from AnchorModel.views import open_broadcast, close_broadcast, register_anchor, follow_anchor, init_broadcast, \
    has_live_permission
from RoomModel.views import fetch_rooms, watch_program, init_chat_room
from ylive.admin import init_category, init_user, init_anchor, init_follow, foo
from ylive.view import login, register, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 登录
    url(r'^user/login/$', login),
    # 注册
    url(r'^user/register/$', register),
    # 登出
    url(r'^user/logout/$', logout),
    # 初始化
    url(r'^admin/init/category/$', init_category),
    url(r'^admin/init/user/$', init_user),
    url(r'^admin/init/anchor/$', init_anchor),
    url(r'^admin/init/follow/$', init_follow),
    url(r'^admin/init/chat_room/$', init_chat_room),
    url(r'^admin/init/broadcast/$', init_broadcast),
    # 测试
    url(r'^foo/$', foo),
    # 开播
    url(r'^anchor/broadcast/open/$', open_broadcast),
    url(r'^anchor/broadcast/permission/$', has_live_permission),
    # 关播
    url(r'^anchor/broadcast/close/$', close_broadcast),
    # 获取房间列表
    url(r'^program/(?P<category>[0-9A-Za-z]+)/$', fetch_rooms),
    # 观看直播
    url(r'^program/room/(?P<room_id>[0-9A-Za-z]+)/$', watch_program),
    # 注册主播
    url(r'^anchor/register/$', register_anchor),
    # 关注 取关
    url(r'^anchor/follow/$', follow_anchor),
]
