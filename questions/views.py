from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, SAFE_METHODS
from questions.models import Question, Answer, AnswerVote, QuestionComment
from questions.serializers import QuestionSerializer, CreateUpdateQuestionSerializer, \
    AnswerSerializer, CreateUpdateAnswerSerializer, AnswerVoteSerializer, QuestionCommentSerializer,\
    CreateUpdateQuestionCommentSerializer, UserSerializer
from questions.permissions import IsAuthorOrReadOnly, IsAuthor
from users.models import CustomUser


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

    @action(detail=True, methods=['GET', 'HEAD', 'OPTIONS'])
    def get_answers(self, request, *args, **kwargs):
        question = self.get_object()
        answers = Answer.objects.\
            select_related('author', 'question').filter(
                question=question).all()
        serializer = AnswerSerializer(
            answers, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'HEAD', 'OPTIONS'])
    def get_comments(self, request, *args, **kwargs):
        question = self.get_object()
        comments = QuestionComment.objects.\
            select_related('author', 'question').\
            filter(question=question).all()
        serializer = QuestionCommentSerializer(comments, many=True,
                                               context={'request': request})
        return Response(serializer.data)


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


class QuestionCommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        question_pk = self.kwargs['question_pk']
        question = Question.objects.filter(pk=question_pk).first()
        if not question:
            raise NotFound(
                detail=f"Question with id {question_pk} was not found.")
        return QuestionComment.objects.select_related('question', 'author').\
            filter(question=question)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return QuestionCommentSerializer
        else:
            return CreateUpdateQuestionCommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            question_id=self.kwargs['question_pk'],
            author_id=self.request.user.id
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all().filter(is_superuser=False)
    filter_backends = [filters.SearchFilter,
                       filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['username']
    ordering_fields = ['id', 'username']

    @action(detail=True, methods=['GET', 'HEAD', 'OPTIONS'])
    def get_questions(self, request, *args, **kwargs):
        user = self.get_object()
        questions = Question.objects.\
            select_related('author').prefetch_related('tags').\
            filter(author=user).all()
        serializer = QuestionSerializer(
            questions, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'HEAD', 'OPTIONS'])
    def get_answers(self, request, *args, **kwargs):
        user = self.get_object()
        answers = Answer.objects.\
            select_related('author', 'question').\
            filter(author=user).all()
        serializer = AnswerSerializer(
            answers, many=True, context={'request': request}
        )
        return Response(serializer.data)
