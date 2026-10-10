import requests
import pandas as pd

pokemon = []
for i in range (1, 1026):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}')
    data = response.json()

    types = [t["type"]["name"] for t in data["types"]]
    entry = {"id": data["id"], "name": data["name"], "types": ", ".join(types)}

    for s in data["stats"]:
        entry[s["stat"]["name"]] = s["base_stat"]
    
    pokemon.append(entry)

pd.DataFrame(pokemon).to_csv("pokemon.csv", index=False)