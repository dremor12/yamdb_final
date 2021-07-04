from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import Title

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, attrs):
        attrs['title'] = get_object_or_404(
            Title,
            id=self.context['view'].kwargs['title_id']
        )
        if not self.partial and Review.objects.filter(
                title=attrs['title'],
                author=self.context['request'].user).exists():
            raise ValidationError({
                'author': 'Вы уже оставляли отзыв на это произведение'
            })
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
