# Generated by Django 2.2.8 on 2020-07-30 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_artist_artist_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='genre_description',
            field=models.TextField(default='No Description'),
        ),
        migrations.AddField(
            model_name='genre',
            name='genre_slug',
            field=models.CharField(default=1, max_length=200),
        ),
    ]