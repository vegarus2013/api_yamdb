# Generated by Django 2.2.16 on 2022-10-21 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20221021_1732'),
    ]

    operations = [
        migrations.RenameField(
            model_name='titles',
            old_name='categor',
            new_name='category',
        ),
    ]
