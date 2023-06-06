from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from questions.models import Question
from questions.serializers import QuestionSerializer, CreateUpdateQuestionSerializer
from questions.permissions import IsAuthorOrReadOnly


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related('author').all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return QuestionSerializer
        else:
            return CreateUpdateQuestionSerializer
