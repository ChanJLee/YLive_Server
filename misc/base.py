from django.http import JsonResponse
from django.http import QueryDict
from rest_framework import serializers


class Json:
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data


class JsonSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.CharField(max_length=20)

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
