import csv
from django.core.management.base import BaseCommand
from reviews.models import User


class Command(BaseCommand):
    help = 'import users'

    def handle(self, *args, **options):
        with open('static/data/users.csv') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                pk = row['id']
                username = row['username']
                email = row['email']
                role = row['role']
                bio = row['bio']
                first_name = row['first_name']
                last_name = row['last_name']

                models = User(username=username,
                              pk=pk,
                              email=email,
                              role=role,
                              bio=bio,
                              first_name=first_name,
                              last_name=last_name,
                              )
                models.save()
        print("Импорт пользователей завершен")
