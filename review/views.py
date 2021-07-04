from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.models import Title

from .models import Comment, Review
from .permissions import IsAuthorOrStaff
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaff]
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get_queryset(self):
        get_object_or_404(Title, pk=self.kwargs['title_id'])
        return self.queryset.filter(title_id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrStaff]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        comments = Comment.objects.filter(review=review)
        return comments

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)
