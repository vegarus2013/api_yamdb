import csv
from django.core.management.base import BaseCommand
from rest_framework.generics import get_object_or_404
from reviews.models import Comment, User, Reviews


class Command(BaseCommand):
    help = 'import commentary'

    def handle(self, *args, **options):
        with open('static/data/comments.csv',
                  encoding="utf-8-sig") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                review_id = row['review_id']
                text = row['text']
                pub_date = row['pub_date']

                author = get_object_or_404(
                    User,
                    pk=row['author']
                )
                review_id = get_object_or_404(
                    Reviews,
                    pk=row['review_id']
                )

                models = Comment(
                    reviews=review_id,
                    text=text,
                    author=author,
                    pub_date=pub_date,
                )
                models.save()
        print("Импорт комментариев завершен")
