from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import YaUser
from api_yamdb.constants import (
    NAME_FIELD_LENGTH,
    SLUG_FIELD_LENGTH,
    REVIEW_MIN_RATE,
    REVIEW_MAX_RATE
)


class Category(models.Model):
    name = models.CharField(max_length=NAME_FIELD_LENGTH)
    slug = models.SlugField(max_length=SLUG_FIELD_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=NAME_FIELD_LENGTH)
    slug = models.SlugField(max_length=SLUG_FIELD_LENGTH, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=NAME_FIELD_LENGTH)
    year = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenreTitle'
    )
    rating = models.IntegerField(default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        YaUser,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                REVIEW_MIN_RATE,
                message=f"Минимальная возможная оценка: {REVIEW_MIN_RATE}.",
            ),
            MaxValueValidator(
                REVIEW_MAX_RATE,
                message=f"Максимальная возможная оценка: {REVIEW_MAX_RATE}.",
            ),
        ],
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        YaUser,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
