from django.shortcuts import render
from profiles_api import models, serializers, permissions
from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import uuid
from profiles_api.helpers import send_forget_password_mail

# Create your views here.

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email', )

class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class NicknameAPIView(APIView):
    serializer_class = serializers.NicknameSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, format = None):
        nickname = request.user.nickname
        return Response({'Nickname' : nickname})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            nickname = serializer.validated_data.get('nickname')
            user_entry = models.UserProfile.objects.get(id = request.user.id)
            user_entry.nickname=nickname
            user_entry.save()
            return Response({'message' : 'nickname changed'})
        else :
            return Response(
                serializer.errors,
                status= status.HTTP_400_BAD_REQUEST
            )

class DeleteUserAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )

    def get(self, request, format = None):
        try:
            user_obj = models.UserProfile.objects.get(email = request.query_params['email']).delete()
            return Response({"message" : "The book record has been deleted successfully."})
        except Exception as e:
            return Response({"error": str(e)})

class MakeAdminAPIView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminUser, )

    def get(self, request, format = None):
        try:
            user_obj = models.UserProfile.objects.get(email = request.query_params['email'])
            user_obj.is_staff = True
            user_obj.save()
            return Response({"message" : "Admin Access Granted"})
        except Exception as e:
            return Response({"error": str(e)})

class ForgetPassword(APIView):
    serializer_class = serializers.ForgetPasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            email = serializer.initial_data['email']
            
            if not models.UserProfile.objects.filter(email=email).first():
                return Response({'message' : 'No user found with this email.'})
            
            user_obj = models.UserProfile.objects.get(email = email)
            token = str(uuid.uuid4())

            if models.TokenModel.objects.filter(user = user_obj).exists():
                profile_obj= models.TokenModel.objects.get(user = user_obj)
            else:
                profile_obj= models.TokenModel.objects.create(user = user_obj)

            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email , token)
            return Response({"message" : "Email sent with reset password link."})
        
        except Exception as e:
            return Response({"error": str(e)})

class ChangePassword(APIView):
    serializer_class = serializers.ResetPasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            profile_obj = models.TokenModel.objects.filter(forget_password_token = request.query_params['token']).first()
            if serializer.is_valid():
                new_password = serializer.validated_data.get('NewPassword')
                confirm_password = serializer.validated_data.get('ConfirmPassword')
                user_id = profile_obj.user.id
                
                if user_id is  None:
                    return Response({"message" : "No user id found."})
                
                if  new_password != confirm_password:
                    return Response({"message" : "Password not same."})
                            
                
                user_obj = models.UserProfile.objects.get(id = user_id)
                user_obj.set_password(new_password)
                user_obj.save()
                return Response({"message" : "Password changed successfully."})
            
        except Exception as e:
            return Response({"error": str(e)})