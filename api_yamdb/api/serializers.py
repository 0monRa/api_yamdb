from rest_framework import serializers

from api_yamdb.constants import NAME_FIELD_LENGTH
from reviews.models import (
    Category,
    Genre,
    Title,
    GenreTitle,
    Review,
    Comment
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        return obj.rating if obj.rating > 0 else None


class TitlePostSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=NAME_FIELD_LENGTH,
        required=True)
    description = serializers.CharField(
        required=False,
        allow_blank=True)
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        many=True,
        queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(
        slug_field='slug',
        read_only=False,
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            GenreTitle.objects.create(genre=genre, title=title)
        return title


class TitleDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'text', 'author', 'score', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'review', 'text', 'author', 'pub_date']
