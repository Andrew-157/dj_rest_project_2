from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from questions.models import Question
from questions.serializers import QuestionSerializer, CreateUpdateQuestionSerializer
from questions.permissions import IsAuthorOrReadOnly


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related('author').\
        prefetch_related('tags').all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'slug', 'details', 'tags__name', 'tags__slug']
    ordering_fields = ['title', 'slug', 'details',
                       'published', 'tags__name', 'tags__slug']

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return QuestionSerializer
        else:
            return CreateUpdateQuestionSerializer
