from django.shortcuts import render
from profiles_api import models, serializers, permissions
from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

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