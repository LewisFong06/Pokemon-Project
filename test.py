import json
import pandas as pd

with open("type_chart.json") as f:
    chart = json.load(f)

def get_matchups(types):
    result = {}
    for attacker in chart["normal"]:
        multiplier = 1
        for t in types:
            multiplier = multiplier * chart[t][attacker]
        result[attacker] = multiplier
    return result

pokemon = pd.read_csv("pokemon.csv")

row = pokemon[pokemon["name"] == "pikachu"].iloc[0]
types = row["types"].split(", ")

print(types)
matchups = get_matchups(types)

weaknesses = []
for attacker, multiplier in matchups.items():
    if multiplier > 1:
        weaknesses.append(attacker)

print(weaknesses)