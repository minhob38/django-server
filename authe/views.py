from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import jwt
from .models import User
import json
from django.utils import timezone
import os
import bcrypt
from django.core import serializers
from datetime import datetime, timedelta

@csrf_exempt
def signup(request):
    try:
        if request.method == "POST":
            body = json.loads(request.body)
            email = body["email"]
            password = body["password"]

            is_user = User.objects.filter(email=email).exists()
            if is_user:
                data = { "status": "error", "message": "user already exists" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(password.encode("utf-8"), salt)
            print(hash, hash.decode("utf-8"))
            user = User(email=email, password=hash.decode("utf-8"), created_at=timezone.now())
            user.save()
            data = {"status": "success", "message": "user signed up"}
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = { "status": "error", "message": str(e) }
        return HttpResponseServerError(json.dumps(data), content_type="application/json")

@csrf_exempt
def signin(request):
    try:
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]

            user = User.objects.filter(email=email)
            is_user = user.exists()

            if not is_user:
                data = { "status": "error", "message": "user does not exist" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            hashed = user.values("password").first()["password"]
            is_match = bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
            if not is_match:
                data = { "status": "error", "message": "password is invalid" }
                return HttpResponseBadRequest(json.dumps(data), content_type="application/json")

            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
            access_token = jwt.encode(
                {
                    "email": email,
                    "iat": datetime.utcnow(),
                    "exp": datetime.utcnow() + timedelta(days=14)
                },
                JWT_SECRET_KEY,
                algorithm="HS256"
            )

            data = {
                "status": "success",
                "message": "user signed in",
                "access_token": access_token
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = { "status": "error", "message": str(e) }
        return HttpResponseServerError(json.dumps(data), content_type="application/json")

def users(request):
    try:
        if request.method == "GET":
            case = 1
            if case == 1:
                # queryest -> json #1
                users = json.loads(serializers.serialize("json", User.objects.all()))
                data = {"status": "success", "message": "found users",  "data": users}
                return HttpResponse(json.dumps(data), content_type="application/json")
            elif case == 2:
                # queryest -> json #2
                users = User.objects.all().values("email")
                data = { "status": "success", "message": "found users",  "data": list(users) }
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                # queryest -> json #3
                users = [{
                    "email": user["email"],
                    "created_at": user["created_at"].strftime("%Y-%m-%d")
                } for user in User.objects.all().values()]
                data = { "status": "success", "message": "found users",  "data": users }
                return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data = { "status": "error", "message": str(e) }
        return HttpResponseServerError(json.dumps(data), content_type="application/json")

### social signup / login
### signout
### admin (settings.py)
### map (class view, postgresql gis, jwt)
### refresh token (redis)
### test code
### lint
### docker
### swagger