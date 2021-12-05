from django import views
from django.http import HttpResponse
from django.views import View
import json

class MapView(View):
    def get(self, request):
        data = {
            "status": "success",
            "message": "user signed up",
        }

        return HttpResponse(json.dumps(data), content_type="application/json")