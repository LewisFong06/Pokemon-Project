import requests

response = requests.get('https://pokeapi.co/api/v2/pokemon/infernape')
data = response.json()

entry = {"name": data["name"]}

for s in data["stats"]:
    entry[s["stat"]["name"]] = s["base_stat"]

print(entry)