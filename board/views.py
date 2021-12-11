from django.shortcuts import render

# Create your views here.
from django import views
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse, request
from django.views import View
import json
from .models import Posts
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostsSerializer

# 게시판 관리 (전체 조회 / 전체 삭제) - APIView 기반 CBV
class BoardView(APIView): #mixed in으로 바꾸기
    """
    게시판 관리
    ---
    단일 게시글을 생성, 전체 게시글 조회/삭제합니다.
    """
    def get(self, request):
        """
        전체 게시글 조회
        ---
        전체 게시글을 조회합니다.
        """
        try:
            serializer = PostsSerializer(Posts.objects.all(), many=True)
            data = {
                "status": "success",
                "message": "found all posts",
                "data": serializer.data
            }
            # https://docs.djangoproject.com/en/3.2/ref/request-response/#jsonresponse-objects
            return JsonResponse(data, status=200, content_type="application/json")
        except Exception as e:
            data = { "status": "success", "message": str(e) }
            return JsonResponse(data, status=500, content_type="application/json")

    def post(self, request):
        """
        단일 게시글 생성
        ---
        단일 게시글을 생성합니다.
        """
        try:
            # https://www.django-rest-framework.org/api-guide/serializers/
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

    def delete(self, request):
        """
        전체 게시글 삭제
        ---
        전체 게시글을 삭제합니다.
        """
        try:
            posts = Posts.objects.all()
            posts.delete()
            data = {
                "status": "success",
                "message": "deleted all posts",
            }
            # https://www.django-rest-framework.org/api-guide/responses/
            return Response(data, status=200, content_type="application/json")
        except Exception as e:
            data = { "status": "success", "message": str(e) }
            return Response(data, status=500, content_type="application/json")

# 게시글 관리 (단일 게시글 조회 / 수정 / 삭제) - APIView 기반 CBV
class PostView(APIView):
    def get(self, request, post_id):
        try:
            # ↓ 아래와 같음, serializer = PostsSerializer(Posts.objects.get(id=post_id), many=False)
            serializer = PostsSerializer(Posts.objects.filter(id=post_id).first(), many=False)
            data = {
                "status": "success",
                "message": "found post",
                "data": serializer.data
            }
            return Response(data, status=200, content_type="application/json")
        except Exception as e:
            data = { "status": "success", "message": str(e) }
        return Response(data, status=500, content_type="application/json")

    @swagger_auto_schema(tags=["board"], request_body=PostsSerializer)
    def patch(self, request, post_id):
        try:
            # https://www.django-rest-framework.org/api-guide/serializers/#partial-updates
            serializer = PostsSerializer(Posts.objects.filter(id=post_id).first(), data=request.POST, partial=True)

            if serializer.is_valid():
                serializer.save()
                data = { "status": "success", "message": "edited post" }
                return Response(data, status=201)

            data = { "status": "error", "message": "bad request" }
            return Response(data, status=400, content_type="application/json")
        except Exception as e:
            data = { "status": "error", "message": str(e) }
            return Response(data, status=500, content_type="application/json")

    @swagger_auto_schema(tags=["board"], request_body=PostsSerializer)
    def put(self, request, post_id):
        try:
            serializer = PostsSerializer(Posts.objects.filter(id=post_id).first(), data=request.POST)

            if serializer.is_valid():
                serializer.save()
                data = { "status": "success", "message": "changed post" }
                return Response(data, status=201)

            data = { "status": "error", "message": "bad request" }
            return Response(data, status=400, content_type="application/json")
        except Exception as e:
            data = { "status": "error", "message": str(e) }
            return Response(data, status=500, content_type="application/json")

    def delete(self, request, post_id):
        try:
            post = Posts.objects.filter(id=post_id).first()
            post.delete()

            data = { "status": "success", "message": "deleted post" }
            return Response(data, status=200)
        except Exception as e:
            data = { "status": "error", "message": str(e) }
            return Response(data, status=500, content_type="application/json")

"""
viewsets 기반 CBV
"""