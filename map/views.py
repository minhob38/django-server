from django import views
from django.http import HttpResponse
from django.views import View
import json
from .models import SeoulSgg
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SeoulSggSerializer

class MapView(APIView):
    def get(self, request):

        seoul_sgg = SeoulSgg.objects.raw("SELECT gid, st_astext(geom) as geom_text FROM SEOUL_SGG")
        serializer = SeoulSggSerializer(seoul_sgg, many=True)

        data = {
            "status": "success",
            "message": "found features",
            "data": serializer.data
        }

        return HttpResponse(json.dumps(data), content_type="application/json")
