from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,\
    UserSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserCreateSerializer):

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id', 'username', 'email', 'password', 'user_image'
        ]


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = [
            'id', 'username', 'email', 'user_image'
        ]
