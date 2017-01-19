from django.http import JsonResponse
from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    def createResponse(self):
        return JsonResponse(data=self.data, safe=False)