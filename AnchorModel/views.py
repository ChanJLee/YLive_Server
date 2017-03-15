# coding=utf-8
import os
from operator import eq

from django.http import QueryDict

from AnchorModel.models import Anchor
from CategoryModel.models import CategoryModel
from RoomModel.models import RoomModel
from decor.decor import put_only, login_required, return_error, return_message
from misc.base import DIR

CATEGORY_SHOW = 0x0521
CATEGORY_SPORT = 0x0522
CATEGORY_PET = 0x0523
CATEGORY_MUSIC = 0x0524
CATEGORY_DESKTOP_GAME = 0x0525
KEY_CATEGORY = u"category"
KEY_TITLE = u"title"

CATEGORY_MAP = {
    CATEGORY_SHOW: u"星秀",
    CATEGORY_SPORT: u"户外",
    CATEGORY_MUSIC: u"音乐",
    CATEGORY_PET: u"宠物",
    CATEGORY_DESKTOP_GAME: u"桌游"
}

'''
开播

put

form:
category
title

{
    "code": 768,
    "message": "你已经开播了",
    "data": null
}
'''


@put_only
@login_required
def open_broadcast(request, *arg, **kwargs):
    user = request.user

    anchor = Anchor.objects.get(user=user)
    if anchor is None:
        return return_error(u"你还不是主播，请申请后再开播")

    try:
        RoomModel.objects.get(ownerId=anchor)
        return return_error(u'你已经开播了')
    except Exception as e:
        pass

    put = QueryDict(request.body)

    if KEY_CATEGORY not in put:
        return return_error(u"类别有误")

    category = put[KEY_CATEGORY]
    if not category or not CATEGORY_MAP[int(category)]:
        return return_error(u"类别有误")

    title = put[KEY_TITLE]
    if not title:
        return return_error(u"标题不能为空")

    category_name = CATEGORY_MAP[int(category)]
    try:
        category = CategoryModel.objects.get(name=category_name)
    except Exception as e:
        print e.message
        return return_error(u"类别有误")
    open_broadcast_impl(user, anchor, category, title)
    return return_message(u"开播成功")


def open_broadcast_impl(user, anchor, category, title):
    write_snapshot(category.name, user.username)
    room = RoomModel()
    room.title = title
    room.categoryId = category
    room.ownerId = anchor
    room.save()


def write_snapshot(category, username):
    if eq(category, u'音乐'):
        dir_name = 'music'
    elif eq(category, u'户外'):
        dir_name = 'sport'
    elif eq(category, u'星秀'):
        dir_name = 'show'
    elif eq(category, u'桌游'):
        dir_name = 'desktop_game'
    else:
        dir_name = 'pet'

    src_dir = DIR + dir_name + '_poll'
    des_dir = DIR + dir_name

    files = os.listdir(src_dir)
    if not files or len(files) < 2:
        return
    print files

    src_path = src_dir + '/' + files[1]
    des_path = des_dir + "/" + username + '.jpg'
    if os.path.exists(des_path):
        return

    src_file = open(src_path, 'rb')
    des_file = open(des_path, 'wb')

    image = src_file.read()
    des_file.write(image)
    src_file.close()
    des_file.flush()
    des_file.close()
    os.remove(src_path)


'''
put

{
    "code": 512,
    "message": "关播成功",
    "data": null
}
'''


@put_only
@login_required
def close_broadcast(request, *arg, **kwargs):
    user = request.user
    anchor = Anchor.objects.filter(user=user)
    if anchor is None:
        return return_error(u"你还不是主播，请申请后再开播")
    try:
        room = RoomModel.objects.get(ownerId=anchor)
        room.delete()
        return return_message(u'关播成功')
    except:
        return return_message(u"你还没有开播")
