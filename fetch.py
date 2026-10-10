import requests
import pandas as pd

pokemon = []
for i in range (1, 1026):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}')
    data = response.json()

    types = [t["type"]["name"] for t in data["types"]]
    pokemon.append({"id": data["id"], "name": data["name"], "types": ", ".join(types)})
    print(f"Fetched data for Pokémon ID {data['id']}: {data['name']}")

pd.DataFrame(pokemon).to_csv("pokemon.csv", index=False)