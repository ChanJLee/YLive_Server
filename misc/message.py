from rest_framework import serializers

from misc.base import BaseSerializer
from misc.error import CODE_OK


class Message:
    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.data = None


class MessageSerializer(BaseSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    code = serializers.IntegerField(default=CODE_OK)
    message = serializers.CharField(max_length=50)
    data = serializers.DictField(required=False)
