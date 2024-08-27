import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import YaUser
from api_yamdb.constants import (
    NAME_FIELD_LENGTH,
    SLUG_FIELD_LENGTH,
    REVIEW_MIN_RATE,
    REVIEW_MAX_RATE,
)
from .constants import TEXT_MAX_LENGTH


class Category(models.Model):
    name = models.CharField(
        max_length=NAME_FIELD_LENGTH, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=SLUG_FIELD_LENGTH,
        unique=True,
        verbose_name='Короткое имя в формате slug',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=NAME_FIELD_LENGTH, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=SLUG_FIELD_LENGTH,
        unique=True,
        verbose_name='Короткое имя в формате slug',
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=NAME_FIELD_LENGTH, verbose_name='Название'
    )
    year = models.PositiveSmallIntegerField(
        default=0,
        db_index=True,
        validators=[
            MaxValueValidator(datetime.date.today().year),
        ],
        verbose_name='Год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', through='GenreTitle', verbose_name='Жанр'
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Заголовок'
    )

    class Meta:
        ordering = ('genre__name',)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Заголовок',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        YaUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(REVIEW_MIN_RATE),
            MaxValueValidator(REVIEW_MAX_RATE),
        ],
        verbose_name='Рейтинг',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:TEXT_MAX_LENGTH]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор',
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        YaUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_MAX_LENGTH]
