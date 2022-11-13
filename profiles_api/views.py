from django.shortcuts import render
from profiles_api import models, serializers
from rest_framework import viewsets

# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating, creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()