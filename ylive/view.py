from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from decor.decor import post_only


@csrf_exempt
@post_only
def login(request):
    if request.method == 'PUT':
        return
    return HttpResponse("put")