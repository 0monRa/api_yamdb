from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (
    CharFilter,
    DjangoFilterBackend,
    FilterSet,
)
from rest_framework import filters, mixins, status, serializers, viewsets
from rest_framework.response import Response

from .mixins import PermissionsMixin
from .serializers import (
    CategorySerializer,
    TitleSerializer,
    TitlePostSerializer,
    TitleDeleteSerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from reviews.models import Category, Genre, Title, Review, Comment
from users.permissions import (
    AdministratorPermission,
    CustomReviewCommentPermission
)


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        fields = ('name', 'year', 'category', 'genre')
        model = Title


class TitleViewSet(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (AdministratorPermission,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializer
        elif self.request.method == 'DELETE':
            return TitleDeleteSerializer
        else:
            return TitlePostSerializer

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class CategoryViewSet(
    PermissionsMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdministratorPermission,)
    lookup_field = 'slug'


class GenreViewSet(
    PermissionsMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdministratorPermission,)
    lookup_field = 'slug'


class ReviewViewSet(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (CustomReviewCommentPermission,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        if Review.objects.filter(
            author=self.request.user,
            title=title
        ).exists():
            raise serializers.ValidationError(
                "Вы уже оставили отзыв на этот заголовок."
            )
        serializer.save(
            author=self.request.user,
            title=title
        )
        title.update_rating()

    def perform_destroy(self, instance):
        title = instance.title
        super().perform_destroy(instance)
        title.update_rating()

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class CommentViewSet(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CustomReviewCommentPermission,)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)
