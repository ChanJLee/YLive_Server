from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    if request.method == 'PUT':
        return
    return HttpResponse("put")