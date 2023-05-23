from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,\
    UserSerializer as BaseUserSerializer
from rest_framework import serializers
from users.models import CustomUser


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id', 'username', 'email', 'password', 'image'
        ]

    def validate_email(self, value):
        # check if user enters email that is not in database
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('Duplicate email')
        return value


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id', 'username', 'email', 'image'
        ]

    def validate_email(self, value):
        # check if user enters email that is either their
        # existing email or new email that is not in the database
        current_user = self.context['request'].user
        user_with_email = CustomUser.objects.filter(email=value).first()
        if user_with_email and user_with_email != current_user:
            raise serializers.ValidationError('Duplicate email')
        return value
