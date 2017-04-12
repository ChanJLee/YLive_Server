# coding=utf-8
import os
from operator import eq

from django.http import QueryDict

from AnchorModel.models import Anchor, UserToAnchorRelationship
from CategoryModel.models import CategoryModel
from RoomModel.models import RoomModel
from decor.decor import put_only, login_required, return_error, return_message, post_only
from misc.base import DIR, log_info

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


def init_broadcast(request):
    category = [0x0521,
                0x0522,
                0x0523,
                0x0524,
                0x0525]
    for c in category:
        x = CATEGORY_MAP[int(c)]
        xx = CategoryModel.objects.get(name=x)
        anchors = Anchor.objects.all()
        count = anchors.count()
        for i in range(20):
            if i > count:
                break
            a = anchors[i]
            open_broadcast_impl(a.user, a, xx, "开播啦")
    return return_message("ok")

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


@post_only
@login_required
def register_anchor(request, *arg, **kwargs):
    user = request.user
    try:
        Anchor.objects.get(user=user)
        return return_error(u"你已经是主播了")
    except Exception as e:
        log_info(register_anchor.__name__, e.message)

    anchor = Anchor(user=user)
    anchor.save()
    return return_message(u"注册成功")


ANCHOR_ID = "anchor_id"

'''
put

{
    "code": 512,
    "message": "关注成功",
    "data": null
}

delete

{
    "code": 512,
    "message": "取关成功",
    "data": null
}
'''


@login_required
def follow_anchor(request, *arg, **kwargs):
    put = QueryDict(request.body)
    if ANCHOR_ID not in put:
        return return_error(u"缺少anchor id")
    if request.method == "PUT":
        return put_follow(request)
    elif request.method == "DELETE":
        return delete_follow(request)
    else:
        return return_error(u"不支持请求")


def put_follow(request):
    put = QueryDict(request.body)
    anchor_id = put[ANCHOR_ID]
    try:
        anchor = Anchor.objects.get(id=anchor_id)
        try:
            UserToAnchorRelationship.objects.get(audience=request.user, anchor=anchor)
            return return_error(u"已经关注过了")
        except:
            pass
        relationship = UserToAnchorRelationship(audience=request.user, anchor=anchor)
        relationship.save()
        return return_message(u"关注成功")
    except Exception as e:
        log_info(put_follow.__name__, e.message)
        return return_error(u"未知错误")


def delete_follow(request):
    put = QueryDict(request.body)
    anchor_id = put[ANCHOR_ID]
    try:
        anchor = Anchor.objects.get(id=anchor_id)
        relationship = UserToAnchorRelationship.objects.get(audience=request.user, anchor=anchor)
        relationship.delete()
        return return_message(u"取关成功")
    except Exception as e:
        log_info(delete_follow.__name__, e.message)
        return return_error(u"还未关注过")
