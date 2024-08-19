import csv
from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title, User


class Command(BaseCommand):
    help = 'Imports data from CSV files into the database'

    def handle(self, *args, **kwargs):
        self.import_categories()
        self.import_genres()
        self.import_titles()
        self.import_users()
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

    def import_categories(self):
        with open(
            'path/to/categories.csv', newline='', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Category.objects.get_or_create(
                    name=row['name'], slug=row['slug']
                )

    def import_genres(self):
        with open(
            'path/to/genres.csv', newline='', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genre.objects.get_or_create(name=row['name'], slug=row['slug'])

    def import_titles(self):
        with open(
            'path/to/titles.csv', newline='', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Category.objects.get(slug=row['category'])
                title = Title.objects.get_or_create(
                    name=row['name'],
                    year=row['year'],
                    description=row['description'],
                    category=category,
                )
                genres = row['genre'].split(',')
                for genre_slug in genres:
                    genre = Genre.objects.get(slug=genre_slug)
                    title.genre.add(genre)

    def import_users(self):
        with open(
            'path/to/users.csv', newline='', encoding='utf-8'
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                User.objects.get_or_create(
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                )
