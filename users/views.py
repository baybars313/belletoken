from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import Userserializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
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
        username=request.data['username']
        password=request.data['password']
        user=User.objects.get(password=password)
        serializer=Userserializer(user)
        
        if user:
            res=Response(
                serializer.data
            )
        else:
            res=Response({"msg": "Invalid password"})
        
        return res
        
class UserView(APIView):
    def get(self, request):
        username=request.data['username']
        user=User.objects.filter(username=username).first()
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
        
