from profiles_api import models
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'nickname', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            nickname=validated_data['nickname'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password) #Hash password 
 
        return super().update(instance, validated_data)

class NicknameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('nickname',)

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)

class ResetPasswordSerializer(serializers.Serializer):
    NewPassword = serializers.CharField(max_length=100)
    ConfirmPassword = serializers.CharField(max_length=100)