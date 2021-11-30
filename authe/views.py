from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup(request):
    return HttpResponse("test", content_type="text/plain")
