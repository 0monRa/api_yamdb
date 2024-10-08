from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.constants import ROLE_FIELD_LENGTH


class YaUser(AbstractUser):
    bio = models.TextField(
        verbose_name='Биография'
    )

    ROLE_ADMIN = 'admin'
    ROLE_MODERATOR = 'moderator'
    ROLE_USER = 'user'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MODERATOR, 'Moderator'),
        (ROLE_USER, 'User'),
    )

    role = models.CharField(
        verbose_name='Пользовательская роль',
        max_length=ROLE_FIELD_LENGTH,
        choices=ROLE_CHOICES,
        default=ROLE_USER
    )

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def clean(self):
        if self.is_superuser and self.is_admin:
            raise ValidationError('Суперпользователь — всегда администратор!')

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.ROLE_ADMIN
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username
