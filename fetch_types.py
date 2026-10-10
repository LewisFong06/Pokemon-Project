import requests
import json

TYPES = ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "fairy"]

chart = {}
for defending in TYPES:
    response = requests.get(f'https://pokeapi.co/api/v2/type/{defending}')
    relations = response.json()["damage_relations"]

    chart[defending] = {attack_type: 1 for attack_type in TYPES}
    for attacker in relations["double_damage_from"]:
        chart[defending][attacker["name"]] = 2
    for attacker in relations["half_damage_from"]:
        chart[defending][attacker["name"]] = 0.5
    for attacker in relations["no_damage_from"]:
        chart[defending][attacker["name"]] = 0

with open("type_chart.json", "w") as f:
    json.dump(chart, f, indent=4)