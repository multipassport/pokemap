from django.db import models
from django.http import request

class Pokemon(models.Model):
    title = models.CharField(verbose_name='Русское имя', max_length=200)
    title_en = models.CharField(
        verbose_name='Английское имя', max_length=200, blank=True
        )
    title_jp = models.CharField(
        verbose_name='Японское имя', max_length=200, blank=True
        )
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(
        verbose_name='Картинка',
        null=True, blank=True,
        upload_to='pokemon_images'
        )
    next_evolution = models.ForeignKey(
        'self',
        verbose_name='Эволюция',
        blank=True, null=True,
        related_name='previous_evolution',
        on_delete=models.SET_NULL
        )

    def __str__(self):
        return self.title

    def get_image_url(self):
        if self.image:
            return self.image.url


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        related_name='pokemon_entities',
        verbose_name='Тип покемона',
        on_delete=models.CASCADE
        )
    latitude = models.FloatField(verbose_name='Широта местоположения', null=True)
    longtitude = models.FloatField(verbose_name='Долгота местоположения', null=True)
    appeared_at = models.DateTimeField(
        verbose_name='Появился в', blank=True, null=True
        )
    dissapeared_at = models.DateTimeField(
        verbose_name='Исчез в', blank=True, null=True
        )
    level = models.IntegerField(verbose_name='Уровень', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True, null=True)
    stregth = models.IntegerField(verbose_name='Атака', blank=True, null=True)
    defence = models.IntegerField(verbose_name='Защита', blank=True, null=True)
    stamina = models.IntegerField(
        verbose_name='Выносливость', blank=True, null=True
        )
