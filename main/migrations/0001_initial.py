# Generated by Django 2.2.8 on 2020-07-21 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_name', models.CharField(max_length=200)),
                ('artist_name', models.CharField(max_length=200)),
                ('release_date', models.DateTimeField(verbose_name='release date')),
                ('album_description', models.TextField()),
            ],
        ),
    ]
