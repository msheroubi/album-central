# Generated by Django 2.2.8 on 2020-07-30 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200729_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='artist_description',
            field=models.TextField(default='No Description'),
        ),
    ]
