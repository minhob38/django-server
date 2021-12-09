from django.shortcuts import render

# Create your views here.
from django import views
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views import View
import json
from .models import Posts
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostsSerializer

# 게시판 관리 (전체 조회 / 전체 삭제)
class BoardView(APIView): #mixed in으로 바꾸기
    def post(self, request):
        try:
            serializer = PostsSerializer(data=request.POST)

            if serializer.is_valid():
                serializer.save()
                data = { "status": "success", "message": "created post" }
                return HttpResponse(json.dumps(data), status=201)

            data = { "status": "success", "message": "bad request" }
            return HttpResponseBadRequest(json.dumps(data), content_type="application/json")
        except Exception as e:
            data = { "status": "error", "message": str(e) }
            return HttpResponseServerError(json.dumps(data), content_type="application/json")

    def get(self, request):
        try:
            serializer = PostsSerializer(Posts.objects.all(), many=True)
            data = {
                "status": "success",
                "message": "found all posts",
                "data": serializer.data
            }
            return Response(data, status=200, content_type="application/json")
        except Exception as e:
            data = { "status": "success", "message": str(e) }
            return Response(data, status=500, content_type="application/json")


        # data = { "status": "success", "message": "post created" }
        # return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

# class PostView()