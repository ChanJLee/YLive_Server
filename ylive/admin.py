# coding=utf-8
from django.contrib.auth.models import User
from django.http import HttpResponse
from numpy import size

from AnchorModel.models import Anchor, UserToAnchorRelationship
from CategoryModel.admin import CategoryModel
from ylive.view import open_broadcast_impl

categories = [u'户外', u'运动', u'科教', u'手游', u'桌游']


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
        user = User.objects.create_user(username, email, password)
        user.save()
    return HttpResponse("add user success")


def update_user():
    for i in range(0, 20):
        username = (u"user%d" % i)
        password = u"1234"
        email = u"wuliyichen@gmail.com"
        user = User.objects.get(username=username)
        user.password = password
        user.email = email
        user.save()
    return HttpResponse("add user success")


def init_anchor(request):
    for user in User.objects.all():
        anchor = Anchor()
        print user.id
        anchor.user = user
        anchor.save()
    return HttpResponse("add anchor success")


def init_follow(request):
    users = User.objects.all()
    anchors = Anchor.objects.all()

    for user in users:
        for anchor in anchors:
            relationship = UserToAnchorRelationship(audience=user, anchor=anchor)
            relationship.save()

    return HttpResponse("init follow success")


def foo(request):
    for x in Anchor.objects.all():
        x.delete()
    users = User.objects.all()
    for user in users:
        try:
            anchor = Anchor()
            anchor.user = user
            anchor.save()
        except Exception as e:
            print e
    categories = CategoryModel.objects.all()
    i = 0
    for category in categories:
        for j in range(0, 20):
            if i >= size(users):
                return HttpResponse("init success")
            user = users[i + 1]
            i += 1
            open_broadcast_impl(user, Anchor.objects.get(user=user), category, u'开播啦~')

    return HttpResponse("init success")
