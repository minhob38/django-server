from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SeoulSggs
from .serializers import SeoulSggsSerializer
from drf_yasg.utils import swagger_auto_schema
from config.swagger_config import MapSwaggerSchema
from django.http import JsonResponse


class SggView(APIView):
    @swagger_auto_schema(
        tags=["map"],
        operation_summary="find all sggs",
        operation_description="find all sggs",
        responses=MapSwaggerSchema.get_sggs_responses,
        deprecated=False,
    )
    def get(self, request):
        try:
            seoul_sggs = SeoulSggs.objects.raw(
                "SELECT gid, st_astext(geom) as geom_text, st_astext(st_centroid(geom)) as center_point FROM seoul_sggs"
            )
            serializer = SeoulSggsSerializer(seoul_sggs, many=True)
            payload = list(
                map(
                    lambda sgg: {
                        "gid": sgg["gid"],
                        "sgg_nm": sgg["sgg_nm"],
                        "center_point": sgg["center_point"],
                    },
                    serializer.data,
                )
            )
            data = {"status": "success", "message": "found sggs", "data": payload}
            return JsonResponse(data, status=200, content_type="application/json")
        except Exception as e:
            data = {"status": "error", "message": str(e)}
            return Response(data, status=500, content_type="application/json")


class SggDetailView(APIView):
    @swagger_auto_schema(
        tags=["map"],
        operation_summary="find sgg",
        operation_description="find sgg with name",
        manual_parameters=MapSwaggerSchema.get_sggs_path_manual_parameters,
        responses=MapSwaggerSchema.get_sggs_path_responses,
        deprecated=False,
    )
    def get(self, request, sgg_nm):
        try:
            # https://docs.djangoproject.com/ko/4.0/topics/db/sql/
            sgg = SeoulSggs.objects.raw(
                "SELECT gid, sgg_nm FROM seoul_sggs WHERE sgg_nm = %s", [sgg_nm]
            )[0]
            payload = {"gid": sgg.gid, "sgg_nm": sgg.sgg_nm}
            data = {"status": "success", "message": "found sgg", "data": payload}
            return Response(data, status=200, content_type="application/json")
        except Exception as e:
            data = {"status": "error", "message": str(e)}
            return Response(data, status=500, content_type="application/json")


class SggBoundView(APIView):
    @swagger_auto_schema(
        tags=["map"],
        operation_summary="find sggs in bound",
        operation_description="find sggs with bound",
        manual_parameters=MapSwaggerSchema.get_sggs_query_manual_parameters,
        responses=MapSwaggerSchema.get_sggs_query_responses,
        deprecated=False,
    )
    def get(self, request):
        try:
            south = request.GET.get("south")
            west = request.GET.get("west")
            notrh = request.GET.get("north")
            east = request.GET.get("east")

            linestring = f"SRID=4326;LINESTRING({west} {south}, {east} {notrh})"

            sggs = SeoulSggs.objects.raw(
                "SELECT gid, sgg_nm FROM seoul_sggs WHERE st_intersects(geom::geometry, %s::geometry)",
                [linestring]
            )
            payload = list(
                map(
                    lambda sgg: {
                        "gid": sgg.gid,
                        "sgg_nm": sgg.sgg_nm,
                    },
                    sggs
                )
            )

            data = {
                "status": "success",
                "message": "found sggs in bound",
                "data": payload
            }
            return Response(data, status=200, content_type="application/json")
        except Exception as e:
            data = {"status": "error", "message": str(e)}
            return Response(data, status=500, content_type="application/json")

# 면적 km2으로 바꾸기
class SggAreaView(APIView):
    @swagger_auto_schema(
        tags=["map"],
        operation_summary="find sggs' area",
        operation_description="find sggs' area by descending order",
        responses=MapSwaggerSchema.get_sggs_areas_responses,
        deprecated=False,
    )
    def get(self, request):
        try:
            # st_area(geom) / 1000000 = km2
            sggs = SeoulSggs.objects.raw(
                "SELECT gid, sgg_nm, st_area(geom) / 1000000 as area FROM seoul_sggs order by area desc"
            )
            payload = list(
                map(
                    lambda sgg: {
                        "gid": sgg.gid,
                        "sgg_nm": sgg.sgg_nm,
                        "area": sgg.area,
                    },
                    sggs,
                )
            )

            data = {
                "status": "success",
                "message": "found sggs's area",
                "data": payload,
            }
            return Response(data, status=200, content_type="application/json")
        except Exception as e:
            data = {"status": "error", "message": str(e)}
            return Response(data, status=500, content_type="application/json")
