# coding=utf-8
from django.contrib.auth.models import User
from django.http import HttpResponse

from AnchorModel.models import Anchor
from CategoryModel.models import CategoryModel

categories = ['户外', '运动', '科教', '手游', '桌游']


def init_category(request):
    for category in categories:
        add_category(category)
    return HttpResponse("success")


def add_category(category):
    model = CategoryModel.objects.create()
    model.name = category
    model.save()


def init_user(request):
    for i in range(0, 20):
        username = ("user%d" % i)
        password = "1234"
        email = "wuliyichen@gmail.com"
        user = User.objects.create_user(username, password, email)
        user.save()
    return HttpResponse("add user success")

def init_anchor(request):
    for user in User.objects.all():
        anchor = Anchor.objects.create()
        anchor.userId = user.id
        anchor.save()
    return HttpResponse("add anchor success")
