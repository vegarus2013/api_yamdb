import csv
from django.core.management.base import BaseCommand
from rest_framework.generics import get_object_or_404
from reviews.models import Reviews, User, Titles


class Command(BaseCommand):
    help = 'import reviews'

    def handle(self, *args, **options):
        with open('static/data/review.csv',
                  encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                text = row['text']
                score = row['score']
                pub_date = row['pub_date']

                author = get_object_or_404(
                    User,
                    pk=row['author']
                )
                title_id = get_object_or_404(
                    Titles,
                    pk=row['title_id']
                )

                models = Reviews(
                    title=title_id,
                    text=text,
                    score=score,
                    author=author,
                    pub_date=pub_date,
                )
                models.save()
        print("Импорт обзоров завершен")
