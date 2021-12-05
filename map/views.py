from django import views
from django.http import HttpResponse
from django.views import View
import json
from .models import SeoulSgg

class MapView(View):
    def get(self, request):
        seoul_sgg = SeoulSgg.objects.all()
        print(seoul_sgg)
        data = {
            "status": "success",
            "message": "found features",
        }

        return HttpResponse(json.dumps(data), content_type="application/json")
