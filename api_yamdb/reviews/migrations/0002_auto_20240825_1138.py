# Generated by Django 3.2 on 2024-08-25 08:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-pub_date',)},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-pub_date',)},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('name',), 'verbose_name': 'произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0, message='Минимальная возможная оценка: 0.'), django.core.validators.MaxValueValidator(100, message='Максимальная возможная оценка: 100.')]),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_author_title'),
        ),
    ]
