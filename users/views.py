from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import Userserializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from django.views.decorators.csrf import csrf_exempt
import jwt, datetime


class RegisterView(APIView):
    def post(self, request):
        serializer=Userserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg":"success"})

# @csrf_exempt
class LoginView(APIView):
    def post(self, request):
        email=request.data['email']
        password=request.data['password']
        user=User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("email not found")

        if user.password != password:
            raise AuthenticationFailed("incorrect password")
        payload={
            "id":user.id,
            "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat":datetime.datetime.utcnow()
        }

        token=jwt.encode(payload, "secret", algorithm="HS256")
        response=Response()
        response.set_cookie(key="jwt", value=token, httponly=False)
        response.data={
            "msg":"success"
        }
        response.cookies['jwt']['samesite'] = 'None'
        response.cookies['jwt']['secure'] = True
        
        return response
        
class UserView(APIView):
    def get(self, request):
        token=request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Uauthorized user")
        try:
            payload=jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("session expired")
        
        user=User.objects.filter(id=payload["id"]).first()
        serializer=Userserializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response=Response()
        response.delete_cookie("jwt")
        response.data={
            "message":"success"
        }
        return response
        
