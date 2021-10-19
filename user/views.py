from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegisterSerializer,UserProfileSerializer,UserPasswordChangeSerializer
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from.models import User
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request,*args,**kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=serializer.validated_data
        data.pop('password2')
        password = data.pop('password')
        user_data = {
            **data,
            "password": password
        }
        user = User.objects.create_user(**user_data)
        user.save()
        # serializer = UserProfileSerializer(user)
        # data = {'user': serializer.data, 'is_admin': user.is_superuser}
        return Response(data, status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    http_method_names = ['post']
    permission_classes = (IsAuthenticated)

    def post(self,request,*args,**kwargs):
        serializer = UserPasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data['phone_number']

        try:
            user = User.objects.get(phone_number=phone_number)
            password = request.data("password")
        except ObjectDoesNotExist:
            return Response("There is no such user! Please register!", status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({"msg": "password has been changed successfully"}, status=status.HTTP_200_OK)


    
class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        ### User will get his or her infos in this endpoint
        """
        return Response(UserProfileSerializer(request.user).data,
                        status=status.HTTP_200_OK)

    def patch(self, request):
        try:
            password = request.data.pop('password')
            user = request.user
            user.set_password(password)
            user.save()
        except:
            pass
        serializer = UserProfileSerializer(
            instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Ma\'lumotlaringiz yangilandi', 'user': serializer.data}, status=status.HTTP_202_ACCEPTED)
  