# encoding=utf-8

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import QueryDict
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from decor.decor import put_only, post_only, return_error, return_message, login_required, CODE_NO_AUTHENTICATION


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
    response = return_message(u"登录成功")
    auth.login(request, user)

    context = {}
    context.update(csrf(request))
    response.set_cookie("csrftoken", context['csrf_token'])
    return response


def authenticate(username=None, password=None):
    try:
        return User.objects.get(username=username, password=password)
    except Exception as e:
        return None


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

