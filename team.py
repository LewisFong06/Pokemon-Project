import json
import pandas as pd

with open("type_chart.json") as f:
    chart = json.load(f)

pokemon = pd.read_csv("pokemon.csv")


def get_types(pokemon_name):
    """ Get the types of the Pokémon from the CSV file """
    row = pokemon[pokemon["name"] == pokemon_name].iloc[0]
    types = row["types"].split(", ")
    return types

def get_matchups(types):
    """ Calculate the damage multipliers for each attacking type against the given defending types"""
    result = {}
    for attacker in chart["normal"]:
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

def team_weaknesses(team):
    """ Count how many Pokémon in the team are weak to each type """
    counts = {attacker: 0 for attacker in chart["normal"]}
    for pokemon_name in team:
        weaknesses = get_weaknesses(pokemon_name)
        for attacker in weaknesses:
            counts[attacker] += 1
    return counts

print(get_weaknesses("infernape"))
print(team_weaknesses(["infernape", "jolteon", "garchomp", "pikachu", "sceptile", "lucario"]))