# coding=utf-8

from django.http import JsonResponse
from django.http import QueryDict
from rest_framework import serializers

DIR = '/Users/chan/Pictures/images/'
DEFAULT_CHAR_LENGTH = 40


class Json:
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data


class JsonSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    code = serializers.IntegerField()
    message = serializers.CharField(max_length=DEFAULT_CHAR_LENGTH)

    def createResponse(self):
        return JsonResponse(data=self.data, safe=False)


def parse_request(request):
    if request.META.get('CONTENT_TYPE', '').startswith('multipart'):
        return parse_multipart(request)
    else:
        return parse_form(request)


def parse_form(request):
    return QueryDict(request.body)


def parse_multipart(request):
    return request.parse_file_upload(request.META, request)


def create_response(code, message, data, response_serializer):
    json = Json(code, message, data)
    return JsonResponse(data=response_serializer(json).data, safe=False)


TAG_INFO = 0x01
TAG_WARNING = 0x02
TAG_ERROR = 0x04


def log_info(where, message):
    log_info(TAG_INFO, where=where, message=message)


def log_warning(where, message):
    log(TAG_WARNING, where=where, message=message)


def log_error(where, message):
    log(TAG_ERROR, where=where, message=message)


def log(tag, message, where=None):
    if tag == TAG_INFO:
        print "i/",
    elif tag == TAG_ERROR:
        print "e/",
    else:
        print "w/",
    if where:
        print where,
    print message
