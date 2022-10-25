# Generated by Django 2.2.16 on 2022-10-24 21:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(9999)]),
        ),
    ]