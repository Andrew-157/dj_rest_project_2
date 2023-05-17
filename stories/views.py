from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from stories.serializers import AuthorSerializer, StorySerializer
from stories.permissions import IsAuthorOrReadOnly
from users.models import CustomUser
from stories.models import Story


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AuthorSerializer


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.select_related('author').all()
    serializer_class = StorySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
