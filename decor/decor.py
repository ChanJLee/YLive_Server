#encoding=utf-8
import json

from django.http import JsonResponse

from misc.code import YLiveResponseCode
from misc.datawrapper import DataWrapper

def post_only(func):
    def func_wrapper(request):
        if not request.method == 'POST':
            error = DataWrapper(YLiveResponseCode.CODE_EXCEPTION, "只支持POST请求", None)
            return JsonResponse(vars(error))
        return func(request)
    return func_wrapper