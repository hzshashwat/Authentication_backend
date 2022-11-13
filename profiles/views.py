from django.shortcuts import render
from rest_framework import viewsets, filters
from profiles import serializers, models, permissions
from rest_framework.authentication import TokenAuthentication


# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )

    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email', 'nickname')