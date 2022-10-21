import csv
from django.core.management.base import BaseCommand
from reviews.models import Categories


class Command(BaseCommand):
    help = 'import category'

    def handle(self, *args, **options):
        with open('static/data/category.csv',
                  encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                name = row['name']
                slug = row['slug']

                models = Categories(name=name, slug=slug)
                models.save()
        print("Импорт категорий завершен")
