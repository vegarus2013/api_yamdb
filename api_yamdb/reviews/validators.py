from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    if year > timezone.now().year:
        raise ValidationError(
            (f'Введенный {year} год не может быть больше текущего!')
        )
