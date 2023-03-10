# Generated by Django 2.2.8 on 2020-08-01 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200731_1926'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre',
            old_name='genre_image',
            new_name='genre_image_url',
        ),
        migrations.AddField(
            model_name='artist',
            name='artist_image_url',
            field=models.CharField(default='https://images.genius.com/6d0fbbc7ce189a8c81671ef92546446e.1000x1000x1.png', max_length=200),
        ),
        migrations.AlterField(
            model_name='album',
            name='album_cover_url',
            field=models.CharField(default='https://assets.genius.com/images/default_cover_image.png?1596138983', max_length=200),
        ),
    ]
