import json
import pandas as pd

with open("type_chart.json") as f:
    chart = json.load(f)

pokemon = pd.read_csv("pokemon.csv")


def get_types(pokemon_name):
    """ Get the types of the Pokémon from the CSV file """
    matches = pokemon[pokemon["name"] == pokemon_name.strip().lower()]
    if matches.empty:
        raise ValueError(f"Pokémon '{pokemon_name}' does not exist.")
    row = matches.iloc[0]
    types = row["types"].split(", ")
    return types

def get_matchups(types):
    """ Calculate the damage multipliers for each attacking type against the given defending types"""
    result = {}
    for attacker in chart:
        multiplier = 1
        for t in types:
            multiplier = multiplier * chart[t][attacker]
        result[attacker] = multiplier
    return result

def get_weaknesses(pokemon_name):
    """ Get the types of the Pokémon and calculate its weaknesses"""
    types = get_types(pokemon_name)
    matchups = get_matchups(types)
    weaknesses = []
    for attacker, multiplier in matchups.items():
        if multiplier > 1:
            weaknesses.append(attacker)
    return weaknesses


def get_resistances(pokemon_name):
    """ Get the types of the Pokémon and calculate its resistances"""
    types = get_types(pokemon_name)
    matchups = get_matchups(types)
    resistances = []
    for attacker, multiplier in matchups.items():
        if multiplier < 1:
            resistances.append(attacker)
    return resistances

def team_weaknesses(team):
    """ Count how many Pokémon in the team are weak to each type """
    counts = {attacker: 0 for attacker in chart}
    for pokemon_name in team:
        weaknesses = get_weaknesses(pokemon_name)
        for attacker in weaknesses:
            counts[attacker] += 1
    return counts

def team_summary(team):
    """ Get the weaknesses and resistances of the team """
    weaknesses = team_weaknesses(team)
    resistances = {attacker: 0 for attacker in chart}
    for pokemon_name in team:
        resists = get_resistances(pokemon_name)
        for attacker in resists:
            resistances[attacker] += 1
    return weaknesses, resistances

team = ["Pikachu", "Charizard", "Blastoise", "Venusaur", "Gengar", "Dragonite"]
weaknesses, resistances = team_summary(team)

for attacker in weaknesses:
    print(f"{attacker}: {weaknesses[attacker]} Pokémon weak to this type, {resistances[attacker]} Pokémon resistant to this type")