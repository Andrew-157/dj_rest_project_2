from rest_framework.exceptions import NotFound
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from stories.serializers import StorySerializer, AuthorSerializer, ReviewSerializer
from stories.models import Story, Review
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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.\
        select_related('author').\
        select_related('story').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        story = Story.objects.filter(pk=self.kwargs['story_pk']).first()
        if not story:
            raise NotFound(detail='Story with this id was not found')
        return Review.objects.\
            select_related('story').\
            select_related('author').\
            filter(story=self.kwargs['story_pk'])

    def get_serializer_context(self):
        return {
            'request': self.request,
            'author_id': self.request.user.id,
            'story_id': self.kwargs['story_pk']
        }
