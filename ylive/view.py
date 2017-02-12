# encoding=utf-8
import os
from operator import eq
from time import timezone

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import QueryDict
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from AnchorModel.models import Anchor
from CategoryModel.admin import CategoryModel
from RoomModel.models import RoomModel
from decor.decor import put_only, post_only, return_error, return_message, login_required
from misc.error import CODE_NO_AUTHENTICATION


@csrf_exempt
@put_only
def login(request, *args, **kwargs):
    put = QueryDict(request.body)
    username = put["username"]
    password = put["password"]

    if not username:
        return return_error(u"用户名不能为空")

    if not password:
        return return_error(u"密码不能为空")
    t = User.objects.get(username='user0', password='1234')
    user = authenticate(username=t.username, password=t.password)
    if user is None:
        return return_error(u"验证失败")
    response = return_message(u"登录成功")
    auth.login(request, user)

    context = {}
    context.update(csrf(request))
    response.set_cookie("csrftoken", context['csrf_token'])
    return response


def authenticate(username=None, password=None):
    return User.objects.get(username=username, password=password)


@put_only
@login_required
def logout(request, *args, **kwargs):
    user = request.user
    if not user and not user.is_authenticated():
        return return_error(u"当前用户并没有登录", code=CODE_NO_AUTHENTICATION)
    auth.logout(request)
    return return_message(u"登出成功")


@csrf_exempt
@post_only
def register(request, *args, **kwargs):
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]

    if not username:
        return return_error(u"用户名不能为空")

    if not password:
        return return_error(u"密码不能为空")

    if not email:
        return return_error(u"邮箱不能为空")

    try:
        user = User.objects.create_user(username, email, password)
        user.save()
    except Exception as e:
        return return_error(u"%s已经被注册" % username)

    return return_message(u"注册成功")


CATEGORY_SHOW = 0x0521
CATEGORY_SPORT = 0x0522
CATEGORY_PET = 0x0523
CATEGORY_MUSIC = 0x0524
CATEGORY_DESKTOP_GAME = 0x0525
KEY_CATEGORY = 'category'
KEY_TITLE = "title"
CATEGORY_MAP = {
    CATEGORY_SHOW: u'星秀',
    CATEGORY_SPORT: u'户外',
    CATEGORY_MUSIC: u'音乐',
    CATEGORY_PET: u'宠物',
    CATEGORY_DESKTOP_GAME: u'桌游'
}


@put_only
@login_required
def open_broadcast(request, *arg, **kwargs):
    user = request.user

    anchor = Anchor.objects.get(user=user)
    if anchor is None:
        return return_error(u"你还不是主播，请申请后再开播")

    put = QueryDict(request.body)

    category = put[KEY_CATEGORY]
    if not category or not CATEGORY_MAP[int(category)]:
        return return_error(u"类别有误")

    title = put[KEY_TITLE]
    if not title:
        return return_error(u"标题不能为空")

    category = CategoryModel.objects.get(name=CATEGORY_MAP[int(category)])
    if not category:
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


DIR = '/Users/chan/Pictures/images/'


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
    des_path = des_dir + "/" + username
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


@put_only
@login_required
def close_broadcast(request, *arg, **kwargs):
    user = request.user
    anchor = Anchor.objects.filter(user=user)
    if anchor is None:
        return return_error(u"你还不是主播，请申请后再开播")
    room = RoomModel.objects.get(ownerId=anchor)
    if not room:
        return return_message(u"你还没有开播")
    room.delete()
    return return_message(u'关播成功')
