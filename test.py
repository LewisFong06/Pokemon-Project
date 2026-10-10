import requests

response = requests.get('https://pokeapi.co/api/v2/type/fire')
data = response.json()

weak_to = [t["name"] for t in data["damage_relations"]["double_damage_from"]]
resists = [t["name"] for t in data["damage_relations"]["half_damage_from"]]
immunes = [t["name"] for t in data["damage_relations"]["no_damage_from"]]

print(weak_to)
print(resists)
print(immunes)