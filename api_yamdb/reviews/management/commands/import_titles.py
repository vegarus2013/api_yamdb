import csv
from django.core.management.base import BaseCommand
from rest_framework.generics import get_object_or_404
from reviews.models import Titles, Categories


class Command(BaseCommand):
    help = 'import titles'

    def handle(self, *args, **options):
        with open('static/data/titles.csv',
                  encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                name = row['name']
                year = row['year']
                category = get_object_or_404(
                    Categories,
                    pk=row['category']
                )

                models = Titles(name=name,
                                year=year,
                                category=category,
                                )
                models.save()
        print("Импорт тайтлов завершен")
