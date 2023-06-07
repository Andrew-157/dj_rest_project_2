from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, SAFE_METHODS
from questions.models import Question, Answer, AnswerVote
from questions.serializers import QuestionSerializer, CreateUpdateQuestionSerializer, \
    AnswerSerializer, CreateUpdateAnswerSerializer, AnswerVoteSerializer
from questions.permissions import IsAuthorOrReadOnly, IsAuthor


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.select_related('author').\
        prefetch_related('tags').all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'slug', 'details', 'tags__name', 'tags__slug']
    ordering_fields = ['title', 'slug', 'details',
                       'published', 'updated', 'tags__name', 'tags__slug']

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return QuestionSerializer
        else:
            return CreateUpdateQuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    # queryset = Answer.objects.\
    #     select_related('author', 'question').all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    serializer_class = AnswerSerializer

    def get_queryset(self):
        question_pk = self.kwargs['question_pk']
        question = Question.objects.filter(pk=question_pk).first()
        if not question:
            raise NotFound(
                detail=f"Question with id {question_pk} was not found.")
        return Answer.objects.select_related('author', 'question').\
            filter(question=question).all()

    def perform_create(self, serializer):
        serializer.save(
            question_id=self.kwargs['question_pk'],
            author_id=self.request.user.id
        )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AnswerSerializer
        else:
            return CreateUpdateAnswerSerializer


class AnswerVoteViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerVoteSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        question_pk = self.kwargs['question_pk']
        answer_pk = self.kwargs['answer_pk']
        question = Question.objects.filter(pk=question_pk).first()
        if not question:
            raise NotFound(
                detail=f'Question with id {question_pk} was not found.')
        answer = Answer.objects.select_related(
            'question').filter(pk=answer_pk).first()
        if not answer or answer.question.id != question.id:
            raise NotFound(
                detail=f'Answer with id {answer.id} was not found for this question.'
            )
        answer_vote = AnswerVote.objects.\
            select_related('answer', 'answer__question').\
            filter(answer=answer, answer__question=question)
        return answer_vote.filter(author=self.request.user)

    def perform_create(self, serializer):
        answer_vote = AnswerVote.objects.filter(answer__id=self.kwargs['answer_pk'],
                                                author=self.request.user).first()
        if answer_vote:
            raise MethodNotAllowed(method='POST',
                                   detail='This user already voted for this answer, vote can be either changed or deleted')
        serializer.save(
            answer_id=self.kwargs['answer_pk'],
            author_id=self.request.user.id
        )
