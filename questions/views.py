# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
# from questions.models import Question, Answer
# from questions.serializers import QuestionSerializer, CreateUpdateQuestionSerializer, AnswerSerializer
# from questions.permissions import IsAuthorOrReadOnly


# class QuestionViewSet(viewsets.ModelViewSet):
#     queryset = Question.objects.select_related('author').all()
#     serializer_class = QuestionSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(author_id=self.request.user.id)

#     def get_serializer_class(self):
#         if self.request.method in SAFE_METHODS:
#             return QuestionSerializer
#         else:
#             return CreateUpdateQuestionSerializer


# class AnswerViewSet(viewsets.ModelViewSet):
#     queryset = Answer.objects.select_related('author', 'question').all()
#     serializer_class = AnswerSerializer
#     permission_classes = [
#         IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
#     ]

#     def perform_create(self, serializer):
#         serializer.save(
#             question_id=self.kwargs['question_pk'],
#             author_id=self.request.user.id
#         )
