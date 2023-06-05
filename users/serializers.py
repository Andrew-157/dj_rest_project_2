from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,\
    UserSerializer as BaseUserSerializer
from rest_framework import serializers


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id', 'username', 'email', 'image', 'password'
        ]

    # def validate_email(self, value):
    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError(detail='Duplicate email')
    #     return value


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id', 'username', 'email', 'image'
        ]

    # def validate_email(self, value):
    #     current_user = self.context['request'].user
    #     user_with_email = User.objects.filter(email=value).first()
    #     if user_with_email and user_with_email != current_user:
    #         raise serializers.ValidationError(detail='Duplicate email')
    #     return value
