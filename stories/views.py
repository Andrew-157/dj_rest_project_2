from django.db.models import Avg
from django.db.models.query_utils import Q
from rest_framework import viewsets, generics, mixins, views
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from stories.serializers import StorySerializer, \
    AuthorSerializer, ReviewsByStorySerializer, ReviewsByAuthorSerializer, \
    RatingsByStorySerializer, RatingsByAuthorSerializer
from stories.models import Story, Review, Rating
from stories.permissions import IsAuthorOrReadOnly
from users.models import CustomUser


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.select_related('author').all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['GET', 'HEAD', 'OPTIONS'])
    def average_rating(self, request, *args, **kwargs):
        story = self.get_object()
        story_average_rating = Rating.objects.\
            filter(story__id=story.id).\
            aggregate(average_rating=Avg('rating'))
        return Response(story_average_rating)


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
                             mixins.DestroyModelMixin,
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


class RatingsByStoryViewSet(viewsets.ModelViewSet):
    # returns ratings left on particular story
    serializer_class = RatingsByStorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    queryset = Rating.objects.\
        select_related('author').\
        select_related('story').\
        all()

    def get_queryset(self):
        story = Story.objects.filter(pk=self.kwargs['story_pk']).first()
        if not story:
            raise NotFound(detail='Story with this id was not found')
        return Rating.objects.\
            select_related('story').\
            select_related('author').\
            filter(story=self.kwargs['story_pk'])

    def get_serializer_context(self):
        return {
            'request': self.request,
            'author_id': self.request.user.id,
            'story_id': self.kwargs['story_pk']
        }

    def create(self, request, *args, **kwargs):
        rating = Rating.objects.filter(
            Q(story__id=self.kwargs['story_pk']) &
            Q(author__id=request.user.id)
        ).first()
        if rating:
            raise MethodNotAllowed(method='POST',
                                   detail='This user already has a rating on this story')
        return super().create(request, *args, **kwargs)


class RatingsByAuthorViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    # returns ratings left by a particular author
    queryset = Rating.objects.\
        select_related('author').\
        select_related('story').all()
    serializer_class = RatingsByAuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        author = CustomUser.objects.filter(pk=self.kwargs['author_pk']).first()
        if not author:
            raise NotFound(detail='Author with this id was not found')
        return Rating.objects.\
            select_related('story').\
            select_related('author').\
            filter(author=self.kwargs['author_pk'])
