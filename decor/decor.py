# encoding=utf-8

from django.http import JsonResponse
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
from misc import error
from misc.error import Error, ErrorSerializer


def post_only(func):
    def func_wrapper(request):
        if not request.method == 'POST':
            err = Error(error.CODE_EXCEPTION, u"只支持POST")
            return ErrorSerializer(err).createResponse()
        return func(request)

    return func_wrapper
