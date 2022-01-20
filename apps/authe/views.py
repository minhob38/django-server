from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core import serializers
from .models import User
import json
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser
from drf_yasg.utils import swagger_auto_schema
from config.utils import create_token, create_hash, get_is_match_password
from config.swagger_config import AuthSwaggerSchema

"""
TODO:
- signup / signin / signout template 만들기 (GET으로 html 응답)
- social signup / signin (google)
- multi login
- refresh token (redis)
"""


@csrf_exempt
# @swaggger_auto_schema document
# https://drf-yasg.readthedocs.io/en/stable/drf_yasg.html#drf_yasg.utils.swagger_auto_schema
# drf_yasgs.openapi document
# https://drf-yasg.readthedocs.io/en/stable/drf_yasg.html#module-drf_yasg.openapi
@swagger_auto_schema(
    tags=["auth"],
    operation_summary="sign up",
    operation_description="sign up with email, password",
    method="post",
    manual_parameters=AuthSwaggerSchema.post_signup_manual_parameters,
    responses=AuthSwaggerSchema.post_signup_responses,
    deprecated=False,
)
@api_view(["POST"])  # swagger를 위해 붙인 decorator
@parser_classes([FormParser])  # swagger를 위해 붙인 decorator
def signup(request):
    try:
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]

            is_user = User.objects.filter(email=email).exists()
            if is_user:
                data = {"status": "error", "message": "user already exists"}
                return HttpResponseBadRequest(
                    json.dumps(data), content_type="application/json"
                )

            hash = create_hash(password)
            user = User(email=email, password=hash, created_at=timezone.now())
            user.save()

            access_token = create_token(email)

            data = {
                "status": "success",
                "message": "user signed up",
                "access_token": access_token,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = {"status": "error", "message": str(e)}
        return HttpResponseServerError(
            json.dumps(data), content_type="application/json"
        )


@csrf_exempt
@swagger_auto_schema(
    tags=["auth"],
    operation_summary="sign in",
    operation_description="sign in with email, password",
    method="post",
    manual_parameters=AuthSwaggerSchema.post_signin_manual_parameters,
    responses=AuthSwaggerSchema.post_signin_responses,
    deprecated=False,
)
@api_view(["POST"])
@parser_classes([FormParser])
def signin(request):
    try:
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]

            user = User.objects.filter(email=email)
            is_user = user.exists()

            if not is_user:
                data = {"status": "error", "message": "user does not exist"}
                return HttpResponseBadRequest(
                    json.dumps(data), content_type="application/json"
                )

            hashed = user.values("password").first()["password"]
            is_match = get_is_match_password(password, hashed)
            if not is_match:
                data = {"status": "error", "message": "password is invalid"}
                return HttpResponseBadRequest(
                    json.dumps(data), content_type="application/json"
                )

            access_token = create_token(email)

            data = {
                "status": "success",
                "message": "user signed in",
                "access_token": access_token,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = {"status": "error", "message": str(e)}
        return HttpResponseServerError(
            json.dumps(data), content_type="application/json"
        )


@swagger_auto_schema(
    method="get",
    operation_summary="find all users",
    operation_description="find all users' email and created_at",
    tags=["auth"],
    responses=AuthSwaggerSchema.get_users_responses,
    deprecated=False,
)
@api_view(["GET"])
def users(request):
    try:
        if request.method == "GET":
            case = 3
            if case == 1:
                # queryest -> json #1
                users = json.loads(serializers.serialize("json", User.objects.all()))
                data = {"status": "success", "message": "found users", "data": users}
                return HttpResponse(json.dumps(data), content_type="application/json")
            elif case == 2:
                # queryest -> json #2
                # values document
                # https://docs.djangoproject.com/en/3.2/ref/models/querysets/#values
                users = User.objects.all().values("email")
                data = {
                    "status": "success",
                    "message": "found users",
                    "data": list(users),
                }
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                # queryest -> json #3
                users = [
                    {
                        "email": user["email"],
                        "created_at": user["created_at"].strftime("%Y-%m-%d"),
                    }
                    for user in User.objects.all().values()
                ]
                data = {"status": "success", "message": "found users", "data": users}
                return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = {"status": "error", "message": str(e)}
        return HttpResponseServerError(
            json.dumps(data), content_type="application/json"
        )


@csrf_exempt
@swagger_auto_schema(
    tags=["auth"],
    operation_summary="change password",
    operation_description="change with new password",
    method="patch",
    request_body=AuthSwaggerSchema.patch_password_request_body,
    responses=AuthSwaggerSchema.patch_password_responses,
    deprecated=False,
)
@api_view(["PATCH"])
def password(request):
    try:
        if request.method == "PATCH":
            email = request.user_info["email"]
            body = json.loads(request.body)
            current_password = body["current_password"]
            new_password = body["new_password"]

            # get으로 바꾸기
            user = User.objects.filter(email=email)
            is_user = user.exists()
            if not is_user:
                data = {"status": "error", "message": "user does not exist"}
                return HttpResponseBadRequest(
                    json.dumps(data), content_type="application/json"
                )

            hashed = user.values("password").first()["password"]
            is_match = get_is_match_password(current_password, hashed)
            if not is_match:
                data = {"status": "error", "message": "password is invalid"}
                return HttpResponseBadRequest(
                    json.dumps(data), content_type="application/json"
                )

            # TODO: current_password == new_password 조건으로 수정
            hashed = user.values("password").first()["password"]
            is_match = get_is_match_password(new_password, hashed)
            if is_match:
                data = {"status": "error", "message": "password is same"}
                return HttpResponseBadRequest(
                    json.dumps(data), content_type="application/json"
                )

            hash = create_hash(new_password)

            user = User.objects.get(email=email)
            user.password = hash
            user.save()

            data = {
                "status": "success",
                "message": "password changed",
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = {"status": "error", "message": str(e)}
        return HttpResponseServerError(
            json.dumps(data), content_type="application/json"
        )


@csrf_exempt
@swagger_auto_schema(
    tags=["auth"],
    operation_summary="sign out",
    operation_description="sign out with password",
    method="delete",
    request_body=AuthSwaggerSchema.delete_signout_request_body,
    responses=AuthSwaggerSchema.delete_signout_responses,
    deprecated=False,
)
@api_view(["DELETE"])
def signout(request):
    try:
        if request.method == "DELETE":
            email = request.user_info["email"]
            body = json.loads(request.body)
            password = body["password"]

            # get으로 바꾸기
            user = User.objects.filter(email=email)
            is_user = user.exists()
            if not is_user:
                data = {"status": "error", "message": "user does not exist"}
                return HttpResponseBadRequest(
                    json.dumps(data), content_type="application/json"
                )

            hashed = user.values("password").first()["password"]
            is_match = get_is_match_password(password, hashed)
            if not is_match:
                data = {"status": "error", "message": "password is invalid"}
                return HttpResponseBadRequest(
                    json.dumps(data), content_type="application/json"
                )

            user = User.objects.get(email=email)
            user.delete()

            data = {
                "status": "success",
                "message": "user signed out",
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = {"status": "error", "message": str(e)}
        return HttpResponseServerError(
            json.dumps(data), content_type="application/json"
        )
