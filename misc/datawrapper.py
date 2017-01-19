#encoding=utf-8
from rest_framework.renderers import JSONRenderer


class DataWrapper(object):
    def __init__(self, code, message, serializer):
        self.code = code
        self.message = message
        self.data = serializer

    def toJsonString(self):
        return "{\"code\":%d,\"message\":\"%s\", \"data\":%s}" % (self.code, self.message, JSONRenderer().render(self.data.data))
