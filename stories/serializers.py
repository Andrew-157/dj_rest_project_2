from rest_framework import serializers
from users.models import CustomUser
from stories.models import Story


class StorySerializer(serializers.HyperlinkedModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True)

    class Meta:
        model = Story
        fields = ['url', 'id', 'title', 'content',
                  'pub_date', 'author_name', 'author']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='author-detail', read_only=True
    )

    stories = serializers.HyperlinkedRelatedField(
        view_name='story-detail',
        many=True,
        read_only=True)

    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username', 'email', 'image', 'stories']
