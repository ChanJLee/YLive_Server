from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from decor.decor import put_only, post_only, return_error


@csrf_exempt
@put_only
def login(request):

    return HttpResponse("put")

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

    user = User.objects.create(username, email, password)
    user.save()

    return HttpResponse()