from rest_framework import serializers
from users.models import CustomUser


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='author-detail'
    )

    class Meta:
        model = CustomUser
        fields = [
            'url', 'id', 'username', 'email', 'image'
        ]
