from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import UserRegisterSrializer,UseLoginSerializer,UserProfileSerializer,UserChagePassSerializer,SendEmailResetPassSerializer,UserPassResetSerializer
from rest_framework import status
from account.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Genrate token manually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# Create UserRegister 

class UserRegister(APIView):
     def post(self,request,format=None):
          serializer = UserRegisterSrializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          user = serializer.save()
          token = get_tokens_for_user(user)
          return Response({'token':token,'msg':'Registration Succefull'},status=status.HTTP_201_CREATED)
     
# login User

class UserLogin(APIView):
     def post(self,request,format=None):
          serializer = UseLoginSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          email=serializer.data.get('email')
          password=serializer.data.get('password')
          user=authenticate(email=email,password=password)
          if user is not None:
               token = get_tokens_for_user(user)
               return Response({'token':token,'msg':'Login  Successfull'},status=status.HTTP_200_OK)
          else:
               return Response({'errors':{'non_field_errors':['Email or password is not correct']}},status=status.HTTP_404_NOT_FOUND)
          
class UserProfile(APIView):
     permission_classes = [IsAuthenticated]  
     def get(self,request,format=None):
          serializer = UserProfileSerializer(request.user)
          return Response(serializer.data,status=status.HTTP_200_OK)
     
class UserChagePass(APIView):
     permission_classes = [IsAuthenticated]  
     def post(self,request,format=None):
          serializer = UserChagePassSerializer(data=request.data,context={'user':request.user})
          serializer.is_valid(raise_exception=True)
          return Response({'msg':'Password change Successfull'},status=status.HTTP_200_OK)
     

class SendEmailResetPass(APIView):
     def post(self,request,format=None):
          serializer = SendEmailResetPassSerializer(data=request.data,context={'user':request.user})
          serializer.is_valid(raise_exception=True)
          return Response({'msg':'Password Reset Link send please chek your mail '},status=status.HTTP_200_OK)
     

class UserPassReset(APIView):
     def post(self,request,uid,token ,format=None):
          serilizer = UserPassResetSerializer(data=request.data,context={'uid':uid,'token':token})
          serilizer.is_valid(raise_exception=True)
          return Response({'msg':'Password Reset Successfull'},status=status.HTTP_200_OK)
   

