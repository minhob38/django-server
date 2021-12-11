from django.shortcuts import render

# Create your views here.
from django import views
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    JsonResponse,
)
import json
from .models import Posts
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostsSerializer
from config.swagger_config import BoardSwaggerSchema

# 게시판 관리 (전체 조회 / 전체 삭제) - APIView 기반 CBV
class BoardView(APIView):  # mixed in으로 바꾸기
    """
    게시판 관리
    ---
    단일 게시글을 생성, 전체 게시글 조회/삭제합니다.
    """

    @swagger_auto_schema(
        tags=["board"],
        operation_summary="find all posts",
        operation_description="find all posts",
        responses=BoardSwaggerSchema.get_posts_responses,
        deprecated=False,
    )
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
                "data": serializer.data,
            }
            # https://docs.djangoproject.com/en/3.2/ref/request-response/#jsonresponse-objects
            return JsonResponse(data, status=200, content_type="application/json")
        except Exception as e:
            data = {"status": "success", "message": str(e)}
            return JsonResponse(data, status=500, content_type="application/json")

    @swagger_auto_schema(
        tags=["board"],
        operation_summary="create post",
        operation_description="create post with author, title, content",
        request_body=PostsSerializer,  # serializer 사용하면, manual_parameter의 form 정의하면 에러 발생
        responses=BoardSwaggerSchema.get_posts_responses,
        deprecated=False,
    )
    def post(self, request):
        """
        단일 게시글 생성
        ---
        단일 게시글을 생성합니다.
        """
        try:
            # https://www.django-rest-framework.org/api-guide/serializers/
            # form으로 보내면, request.data / request.POST에 담김
            # body로 보내면, request.data에 담김
            serializer = PostsSerializer(data=request.data)  # author를 user_info에서 가져오기

            if serializer.is_valid():
                serializer.save()
                data = {"status": "success", "message": "created post"}
                return HttpResponse(json.dumps(data), status=201)

            data = {"status": "success", "message": "bad request"}
            return HttpResponseBadRequest(
                json.dumps(data), content_type="application/json"
            )
        except Exception as e:
            data = {"status": "error", "message": str(e)}
            return HttpResponseServerError(
                json.dumps(data), content_type="application/json"
            )

    @swagger_auto_schema(
        tags=["board"],
        operation_summary="delete all post",
        operation_description="delete all posts",
        responses=BoardSwaggerSchema.delete_posts_responses,
        deprecated=False,
    )
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
            data = {"status": "error", "message": str(e)}
            return Response(data, status=500, content_type="application/json")


# 게시글 관리 (단일 게시글 조회 / 수정 / 삭제) - APIView 기반 CBV
class PostView(APIView):
    @swagger_auto_schema(
        tags=["board"],
        operation_summary="find post",
        operation_description="find post with post id",
        manual_parameters=BoardSwaggerSchema.get_posts_path_manual_parameters,
        responses=BoardSwaggerSchema.get_posts_path_responses,
        deprecated=False,
    )
    def get(self, request, post_id):
        try:
            # ↓ 아래와 같음, serializer = PostsSerializer(Posts.objects.get(id=post_id), many=False)
            serializer = PostsSerializer(
                Posts.objects.filter(id=post_id).first(), many=False
            )
            data = {
                "status": "success",
                "message": "found post",
                "data": serializer.data,
            }
            return Response(data, status=200, content_type="application/json")
        except Exception as e:
            data = {"status": "success", "message": str(e)}
        return Response(data, status=500, content_type="application/json")

    @swagger_auto_schema(
        tags=["board"],
        operation_summary="edit post",
        operation_description="edit post with post id, title, content",
        request_body=PostsSerializer,
        responses=BoardSwaggerSchema.patch_posts_path_responses,
        deprecated=False,
    )
    def patch(self, request, post_id):
        try:
            # https://www.django-rest-framework.org/api-guide/serializers/#partial-updates
            serializer = PostsSerializer(
                Posts.objects.filter(id=post_id).first(),
                data=request.data,
                partial=True,
            )

            if serializer.is_valid():
                serializer.save()
                data = {"status": "success", "message": "edited post"}
                return Response(data, status=201)

            data = {"status": "error", "message": "bad request"}
            return Response(data, status=400, content_type="application/json")
        except Exception as e:
            data = {"status": "error", "message": str(e)}
            return Response(data, status=500, content_type="application/json")

    @swagger_auto_schema(
        tags=["board"],
        operation_summary="change post",
        operation_description="change post with post id, title, content",
        request_body=PostsSerializer,
        responses=BoardSwaggerSchema.put_posts_path_responses,
        deprecated=False,
    )
    def put(self, request, post_id):
        try:
            serializer = PostsSerializer(
                Posts.objects.filter(id=post_id).first(), data=request.data
            )

            if serializer.is_valid():
                serializer.save()
                data = {"status": "success", "message": "changed post"}
                return Response(data, status=201)

            data = {"status": "error", "message": "bad request"}
            return Response(data, status=400, content_type="application/json")
        except Exception as e:
            data = {"status": "error", "message": str(e)}
            return Response(data, status=500, content_type="application/json")

    @swagger_auto_schema(
        tags=["board"],
        operation_summary="delete post",
        operation_description="delete post with post id",
        responses=BoardSwaggerSchema.delete_posts_path_responses,
        deprecated=False,
    )
    def delete(self, request, post_id):
        try:
            post = Posts.objects.filter(id=post_id).first()
            post.delete()

            data = {"status": "success", "message": "deleted post"}
            return Response(data, status=200)
        except Exception as e:
            data = {"status": "error", "message": str(e)}
            return Response(data, status=500, content_type="application/json")


# mixin / genetic / viewset
