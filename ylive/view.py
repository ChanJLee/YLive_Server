# encoding=utf-8

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import QueryDict
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from decor.decor import put_only, post_only, return_error, return_message


@csrf_exempt
@put_only
def login(request):
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
    context = {}
    context.update(csrf(request))
    response.set_cookie("csrftoken", context['csrf_token'])
    return response

@csrf_exempt
@post_only
def register(request):
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
