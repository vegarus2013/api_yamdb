import csv

from django.core.management.base import BaseCommand
from reviews.models import Genre


class Command(BaseCommand):
    help = 'import genre'

    def handle(self, *args, **options):
        with open('static/data/genre.csv',
                  encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                name = row['name']
                slug = row['slug']

                models = Genre(name=name, slug=slug)
                models.save()
        print("Импорт жанров завершен")
