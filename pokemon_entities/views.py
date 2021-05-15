import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.all():
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longtitude,
            request.build_absolute_uri(pokemon_entity.pokemon.get_image_url()),
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.get_image_url()),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    for pokemon in Pokemon.objects.all():
        pokemons = {
            'pokemon_id': pokemon.id,
            'description': pokemon.description,
            'img_url': request.build_absolute_uri(pokemon.get_image_url()),
            'title_ru': pokemon.title,
            'title_en': pokemon.title_en,
            'title_jp': pokemon.title_en,
            }
        if pokemon.next_evolution:
            pokemons['next_evolution'] = {
                'pokemon_id': pokemon.next_evolution.id,
                'title_ru': pokemon.next_evolution.title,
                'img_url': request.build_absolute_uri(
                    pokemon.next_evolution.get_image_url())
                }

        if pokemon.previous_evolution.all():
            pokemons['previous_evolution'] = {
                'pokemon_id': pokemon.previous_evolution.get().id,
                'title_ru': pokemon.previous_evolution.get().title,
                'img_url': request.build_absolute_uri(
                    pokemon.previous_evolution.get().get_image_url())
                }
        if pokemon.id == int(pokemon_id):
            requested_pokemon = Pokemon.objects.get(id=pokemon_id)
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in PokemonEntity.objects.filter(pokemon__id=pokemon_id):
        add_pokemon(
            folium_map, pokemon_entity.latitude,
            pokemon_entity.longtitude,
            request.build_absolute_uri(pokemon.get_image_url()),
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons
    })
