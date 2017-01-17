#encoding=utf-8


class DataWrapper(object):
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data