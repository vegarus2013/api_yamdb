# Generated by Django 2.2.16 on 2022-10-21 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20221020_0415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='titles',
            name='genre',
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Genres')),
                ('title_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Titles')),
            ],
        ),
        migrations.AddField(
            model_name='titles',
            name='genre',
            field=models.ManyToManyField(through='reviews.GenreTitle', to='reviews.Genres'),
        ),
    ]