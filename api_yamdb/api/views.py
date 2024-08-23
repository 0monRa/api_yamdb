from django_filters.rest_framework import (
    CharFilter,
    DjangoFilterBackend,
    FilterSet
)
from rest_framework import viewsets, filters, status
from rest_framework.response import Response

from .serializers import (
    CategorySerializer,
    TitleSerializer,
    TitlePostSerializer,
    TitleDeleteSerializer,
    GenreSerializer,
    ReviewSerializer,
    CommentSerializer
)
from reviews.models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)
from users.permissions import (
    AdministratorPermission,
    AnonymousPermission,
    AuthorPermission,
    ModeratorPermission,
)


class PermissionsMixin:

    def get_permissions(self):
        if self.action in {'list', 'retrieve'}:
            return (AnonymousPermission(),)
        return super().get_permissions()


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


class CategoryViewSet(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdministratorPermission,)


class GenreViewSet(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (AdministratorPermission,)


class ReviewViewSet(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorPermission, ModeratorPermission)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(PermissionsMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorPermission, ModeratorPermission)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
