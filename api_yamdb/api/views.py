# from django.db import csv
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .serializers import (
    CategorySerializer,
    TitleSerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer
)
from reviews.models import Category, Genre, Title, Review, Comment
from users.permissions import UserPermission, AdminPermission


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [UserPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [UserPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
