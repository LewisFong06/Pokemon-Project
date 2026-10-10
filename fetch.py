import requests

response = requests.get('https://pokeapi.co/api/v2/pokemon/infernape')
data = response.json()

print(data["name"])
types = [t["type"]["name"] for t in data["types"]]
print("Types:", ", ".join(types))