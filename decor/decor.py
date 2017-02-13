# encoding=utf-8
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

# class Point:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#
# class PointSerializer(serializers.Serializer):
#     def create(self, validated_data):
#         return Point(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.x = validated_data.get("x", instance.x)
#         instance.y = validated_data.get("y", instance.y)
#         pass
#
#     x = serializers.IntegerField()
#     y = serializers.IntegerField()
#
#
# class Person:
#     def __init__(self, name, age, point):
#         self.name = name
#         self.age = age
#         self.point = point
#
#
# class PersonSerializer(serializers.Serializer):
#     def create(self, validated_data):
#         pass
#
#     def update(self, instance, validated_data):
#         pass
#
#     name = serializers.CharField(max_length=20)
#     age = serializers.IntegerField(default=1000)
#     point = PointSerializer(required=False)

# point = Point(x=100, y=100)
# pointSer = PointSerializer(point)
# parser = JSONParser()
# renderer = JSONRenderer()
# print renderer.render(pointSer.data)
# x = parser.parse(BytesIO(renderer.render(pointSer.data)))
# temp = PointSerializer(data=x)
# temp.is_valid()
# print temp.validated_data["x"]
# person = Person("lee", 20, point)
# s = PersonSerializer(person)
# return JsonResponse(s.data, safe=False)
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
