from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import YaUser

MIN_RATE = 0
MAX_RATE = 100


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True
    )
    genre = models.ManyToManyField(Genre, related_name='titles')
    rating = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    author = models.ForeignKey(YaUser, on_delete=models.CASCADE, related_name="reviews")
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                MIN_RATE,
                message=f"Минимальная возможная оценка: {MIN_RATE}.",
            ),
            MaxValueValidator(
                MAX_RATE,
                message=f"Максимальная возможная оценка: {MAX_RATE}.",
            ),
        ],
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = models.ForeignKey(YaUser, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
