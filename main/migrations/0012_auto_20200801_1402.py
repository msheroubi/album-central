# Generated by Django 2.2.8 on 2020-08-01 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_album_author'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='album',
            unique_together={('artist_name', 'album_name')},
        ),
        migrations.AlterUniqueTogether(
            name='track',
            unique_together={('artist_name', 'track_name')},
        ),
    ]