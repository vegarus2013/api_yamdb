from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Comment, Reviews


class ReviewsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'title', 'pub_date',)
        model = Reviews


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'reviews', 'pub_date',)
        model = Comment
