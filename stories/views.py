from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from stories.serializers import StorySerializer, AuthorSerializer
from stories.models import Story
from stories.permissions import IsAuthorOrReadOnly
from users.models import CustomUser


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.select_related('author').all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AuthorSerializer
