# encoding=utf-8
import base as base
from rest_framework import serializers

CODE_OK = 0x200
CODE_EXCEPTION = 0x300
CODE_NO_AUTHENTICATION = 0x400


class Error:
    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.data = None

class ErrorSerializer(base.BaseSerializer):
    code = serializers.IntegerField(default=CODE_EXCEPTION)
    message = serializers.CharField(max_length=50)
    data = serializers.DictField(required=False)