# from rest_framework import serializers
# from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
# from rest_framework_nested.relations import NestedHyperlinkedIdentityField, NestedHyperlinkedRelatedField
# from questions.models import Question, Answer
# from users.models import CustomUser


# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = [
#             'username', 'image'
#         ]


# class QuestionSerializer(serializers.HyperlinkedModelSerializer):
#     author = AuthorSerializer()

#     class Meta:
#         model = Question
#         fields = [
#             'url', 'id', 'content', 'author', 'published'
#         ]


# class CreateUpdateQuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = [
#             'url', 'id', 'content', 'published'
#         ]


# class AnswerSerializer(NestedHyperlinkedModelSerializer):
#     url = NestedHyperlinkedIdentityField(
#         view_name='question-answer-detail',
#         lookup_field='pk',
#         parent_lookup_kwargs={
#             'question_pk': 'question__pk'
#         }
#     )
#     author = serializers.ReadOnlyField(source='author.username')
#     # author_image = serializers.ImageField(source='author.image')
#     question = serializers.ReadOnlyField(source='question.content')

#     class Meta:
#         model = Answer
#         fields = [
#             'url', 'id', 'content', 'question', 'author', 'published'
#         ]
