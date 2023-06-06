from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedIdentityField, NestedHyperlinkedRelatedField
from questions.models import Question, Tag
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
            'url', 'id', 'author', 'title', 'slug', 'tags', 'details', 'published', 'updated'
        ]


class CreateUpdateQuestionSerializer(serializers.ModelSerializer):
    tags = TagsSerializerField(required=False)

    class Meta:
        model = Question
        fields = [
            'url', 'id', 'title', 'details', 'tags', 'published', 'updated'
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
