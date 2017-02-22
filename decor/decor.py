# encoding=utf-8
from rest_framework import serializers

from misc.base import Json, JsonSerializer

CODE_OK = 0x200
CODE_EXCEPTION = 0x300
CODE_NO_AUTHENTICATION = 0x400


class MessageSerializer(JsonSerializer):
    data = serializers.CharField(required=None)


def return_error(message, code=CODE_EXCEPTION):
    json = Json(code, message, None)
    return MessageSerializer(json).createResponse()


def return_message(message):
    json = Json(CODE_OK, message, None)
    return JsonSerializer(json).createResponse()


def post_only(func):
    def func_wrapper(request, *args, **kwargs):
        if not request.method == 'POST':
            return return_error(u"仅支持POST")
        return func(request, args, kwargs)

    return func_wrapper


def put_only(func):
    def func_wrapper(request, *args, **kwargs):
        if not request.method == 'PUT':
            return return_error(u"仅支持PUT")
        return func(request, args, kwargs)

    return func_wrapper


def delete_only(func):
    def func_wrapper(request, *args, **kwargs):
        if not request.method == "DELETE":
            return return_error(u"仅支持DELETE")
        return func(request, args, kwargs)

    return func_wrapper


def get_only(func):
    def func_wrapper(request, *args, **kwargs):
        if not request.method == "GET":
            return return_error(u"仅支持GET")
        return func(request, args, kwargs)

    return func_wrapper


def login_required(func):
    def func_wrapper(request, *args, **kwargs):
        user = request.user
        if not user and not user.is_authenticated():
            return return_error(u"当前用户并没有登录", code=CODE_NO_AUTHENTICATION)
        return func(request, args, kwargs)

    return func_wrapper
