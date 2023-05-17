from rest_framework import viewsets
from stories.serializers import AuthorSerializer
from users.models import CustomUser


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AuthorSerializer
