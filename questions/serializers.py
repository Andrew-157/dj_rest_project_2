from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedIdentityField, NestedHyperlinkedRelatedField
from questions.models import Question
from users.models import CustomUser


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'image'
        ]


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Question
        fields = [
            'url', 'id', 'author', 'title', 'slug', 'details', 'published'
        ]


class CreateUpdateQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = [
            'url', 'id', 'title', 'details', 'published'
        ]
