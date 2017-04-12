# encoding=utf-8

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import QueryDict
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers

from decor.decor import put_only, post_only, return_error, return_message, login_required, CODE_NO_AUTHENTICATION, \
    CODE_OK
from misc.base import DEFAULT_CHAR_LENGTH, JsonSerializer, create_response
from ylive.settings import STATIC_FILE_SERVER_CONFIG

'''
/user/login/
put

username : user0
password : 1234

{
    "code": 512,
    "message": "登录成功",
    "data": null
}
'''


class UserWrapper:
    def __init__(self, username, email, avatar=None):
        self.username = username
        self.email = email
        self.avatar = avatar


class UserWrapperSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=DEFAULT_CHAR_LENGTH)
    email = serializers.CharField(max_length=DEFAULT_CHAR_LENGTH)
    avatar = serializers.URLField(required=False)


class UserWrapperResponseSerializer(JsonSerializer):
    data = UserWrapperSerializer(required=True)


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
    user = authenticate(username=username, password=password)
    if user is None:
        return return_error(u"验证失败")

    auth.login(request, user)

    user = UserWrapper(username=user.username, email=user.email, avatar=get_avatar_url(user))
    data = UserWrapperSerializer(user).data
    response = create_response(CODE_OK, u"登录成功", data, UserWrapperResponseSerializer)
    context = {}
    context.update(csrf(request))
    response.set_cookie("csrftoken", context['csrf_token'])
    return response


'''
只是暂时做个简单的读取
'''


def get_avatar_url(user):
    return "http://%s:%s/%s/%s.png" % (
        STATIC_FILE_SERVER_CONFIG['ip'], STATIC_FILE_SERVER_CONFIG['port'], "avatar", "avatar");


# def authenticate(username=None, password=None):
#     try:
#         return User.objects.get(username=username)
#     except Exception as e:
#         return None

'''
/user/logout/
put
X-CSRFToken

{
    "code": 512,
    "message": "登出成功",
    "data": null
}
'''


@put_only
@login_required
def logout(request, *args, **kwargs):
    user = request.user
    if not user and not user.is_authenticated():
        return return_error(u"当前用户并没有登录", code=CODE_NO_AUTHENTICATION)
    auth.logout(request)
    return return_message(u"登出成功")


'''
/user/register/
post

username
password
email

{
    "code": 512,
    "message": "注册成功",
    "data": null
}

{
    "code": 768,
    "message": "user0已经被注册",
    "data": null
}
'''


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
