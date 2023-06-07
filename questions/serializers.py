from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedIdentityField, NestedHyperlinkedRelatedField
from questions.models import Question, Tag, Answer, AnswerVote
from users.models import CustomUser


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'image'
        ]


class TagsSerializerField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        return data.values_list('name', flat=True)


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer()
    tags = TagsSerializerField(required=False)

    class Meta:
        model = Question
        fields = [
            'url', 'id', 'author', 'title', 'slug',
            'tags', 'details', 'published', 'updated',
            'answers'
        ]

    answers = serializers.SerializerMethodField(
        method_name='count_answers'
    )

    def count_answers(self, question: Question):
        return Answer.objects.filter(question__id=question.id).count()


class CreateUpdateQuestionSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagsSerializerField(required=False)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Question
        fields = [
            'url', 'id', 'author', 'title', 'details', 'tags', 'published', 'updated'
        ]

    def create(self, validated_data):
        tag_names = validated_data.pop(
            'tags') if "tags" in validated_data else None
        instance = super(CreateUpdateQuestionSerializer,
                         self).create(validated_data)
        if tag_names:
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        tag_names = validated_data.pop(
            'tags') if "tags" in validated_data else None
        instance = super(CreateUpdateQuestionSerializer,
                         self).update(instance, validated_data)
        if tag_names:
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            instance.tags.set(tags)
        return instance


class AnswerSerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='question-answer-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'question_pk': 'question__pk'
        }
    )
    author = AuthorSerializer()
    question = serializers.ReadOnlyField(source='question.title')

    class Meta:
        model = Answer
        fields = [
            'url', 'id', 'question', 'author', 'content', 'published', 'updated'
        ]


class CreateUpdateAnswerSerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='question-answer-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'question_pk': 'question__pk'
        }
    )
    author = serializers.ReadOnlyField(source='author.username')
    question = serializers.ReadOnlyField(source='question.title')

    class Meta:
        model = Answer
        fields = [
            'url', 'id', 'question', 'author', 'content', 'published', 'updated'
        ]


class AnswerVoteSerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='question-answer-vote-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'answer_pk': 'answer__pk',
            'question_pk': 'answer__question__pk'
        }
    )

    # parent_lookup_kwargs = {
    #     'answer_pk': 'answer__pk',
    #     'question_pk': 'answer__question__pk'
    # }

    author = serializers.ReadOnlyField(source='author.username')
    answer = serializers.ReadOnlyField(source='answer.content')

    class Meta:
        model = AnswerVote
        fields = ['url', 'id', 'author', 'answer', 'useful']
