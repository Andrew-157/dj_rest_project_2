from rest_framework.exceptions import NotFound
from rest_framework import viewsets, generics, mixins, views
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from stories.serializers import StorySerializer, AuthorSerializer, ReviewsByStorySerializer, ReviewsByAuthorSerializer
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


class ReviewsByStoryViewSet(viewsets.ModelViewSet):
    # returns reviews left for a particular story
    queryset = Review.objects.\
        select_related('author').\
        select_related('story').all()
    serializer_class = ReviewsByStorySerializer
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


class ReviewsByAuthorViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    # returns reviews by a particular author
    queryset = Review.objects.\
        select_related('author').\
        select_related('story').all()
    serializer_class = ReviewsByAuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        author = CustomUser.objects.filter(pk=self.kwargs['author_pk']).first()
        if not author:
            raise NotFound(detail='Author with this id was not found')
        return Review.objects.\
            select_related('story').\
            select_related('author').\
            filter(author=self.kwargs['author_pk'])
