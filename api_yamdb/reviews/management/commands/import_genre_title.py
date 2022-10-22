import csv
from django.core.management.base import BaseCommand
from reviews.models import GenreTitle


class Command(BaseCommand):
    help = 'import GenreTitle'

    def handle(self, *args, **options):
        with open('static/data/genre_title.csv',
                  encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                title_id = row['title_id']
                genre_id = row['genre_id']

                models = GenreTitle(title_id=title_id, genre_id=genre_id)
                models.save()
        print("Импорт жанров для тайтлов завершен")
