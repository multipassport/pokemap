# Generated by Django 3.1.10 on 2021-05-12 17:47

from django.db import migrations, models
import django.http.request


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0002_auto_20210512_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=django.http.request.HttpRequest.build_absolute_uri),
        ),
    ]