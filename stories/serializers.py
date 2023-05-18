from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from users.models import CustomUser
from stories.models import Story, Review, Rating


class StorySerializer(serializers.HyperlinkedModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True)
    reviews = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='story-review-detail',
        parent_lookup_kwargs={'story_pk': 'story__pk'}
    )

    ratings = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='story-rating-detail',
        parent_lookup_kwargs={'story_pk': 'story__pk'}
    )
    average_rating = serializers.HyperlinkedIdentityField(
        view_name='story-average-rating', read_only=True
    )

    class Meta:
        model = Story
        fields = ['url', 'id', 'title', 'content',
                  'pub_date', 'average_rating', 'author_name', 'author',
                  'reviews', 'ratings']


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='author-detail', read_only=True
    )

    stories = serializers.HyperlinkedRelatedField(
        view_name='story-detail',
        many=True,
        read_only=True)

    reviews = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='author-review-detail',
        parent_lookup_kwargs={'author_pk': 'author__pk'}
    )

    ratings = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='author-rating-detail',
        parent_lookup_kwargs={'author_pk': 'author__pk'}
    )

    class Meta:
        model = CustomUser
        fields = ['url', 'id', 'username',
                  'email', 'image', 'stories', 'reviews', 'ratings']


class ReviewsByStorySerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='story-review-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'story_pk': 'story__pk'
        }
    )
    story_title = serializers.ReadOnlyField(source='story.title')
    story = serializers.HyperlinkedRelatedField(
        view_name='story-detail', read_only=True
    )
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True
    )

    class Meta:
        model = Review
        fields = ['url', 'id', 'content', 'pub_date',
                  'story_title', 'story',
                  'author_name', 'author']

    def create(self, validated_data):
        author_id = self.context['author_id']
        story_id = self.context['story_id']
        return Review.objects.create(
            author_id=author_id,
            story_id=story_id,
            **validated_data
        )


class ReviewsByAuthorSerializer(NestedHyperlinkedModelSerializer):

    url = NestedHyperlinkedIdentityField(
        view_name='author-review-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'author_pk': 'author__pk'
        }
    )
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True
    )
    story_title = serializers.ReadOnlyField(source='story.title')
    story = serializers.HyperlinkedRelatedField(
        view_name='story-detail', read_only=True
    )

    class Meta:
        model = Review
        fields = ['url', 'id', 'content', 'pub_date',
                  'author_name', 'author', 'story_title', 'story']


class RatingsByStorySerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='story-rating-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'story_pk': 'story__pk'
        }
    )
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True
    )
    story_title = serializers.ReadOnlyField(source='story.title')
    story = serializers.HyperlinkedRelatedField(
        view_name='story-detail', read_only=True
    )

    class Meta:
        model = Rating
        fields = ['url', 'id', 'rating', 'pub_date',
                  'author_name', 'author', 'story_title', 'story']

    def create(self, validated_data):
        author_id = self.context['author_id']
        story_id = self.context['story_id']
        return Rating.objects.create(
            author_id=author_id,
            story_id=story_id,
            **validated_data
        )


class RatingsByAuthorSerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='author-rating-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'author_pk': 'author__pk'
        }
    )
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True
    )
    story_title = serializers.ReadOnlyField(source='story.title')
    story = serializers.HyperlinkedRelatedField(
        view_name='story-detail', read_only=True
    )

    class Meta:
        model = Rating
        fields = ['url', 'id', 'rating', 'pub_date',
                  'author_name', 'author', 'story_title', 'story']
