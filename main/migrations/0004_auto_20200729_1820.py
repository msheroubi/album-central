# Generated by Django 2.2.8 on 2020-07-30 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200729_1809'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'verbose_name_plural': 'Albums'},
        ),
        migrations.AlterField(
            model_name='album',
            name='artist_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='main.Artist', verbose_name='Artist'),
        ),
    ]