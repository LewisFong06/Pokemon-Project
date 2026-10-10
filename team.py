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

def get_stats(pokemon_name):
    """ Get the base stats of the Pokemon """
    matches = pokemon[pokemon["name"] == pokemon_name.strip().lower()]
    if matches.empty:
        raise ValueError(f"Pokémon '{pokemon_name}' does not exist.")
    row = matches.iloc[0]
    stats = {
        "hp": row["hp"],
        "attack": row["attack"],
        "defense": row["defense"],
        "special_attack": row["special-attack"],
        "special_defense": row["special-defense"],
        "speed": row["speed"]
    }
    return stats

def get_total_stats(pokemon_name):
    """ Get the total base stats of the Pokemon """
    stats = get_stats(pokemon_name)
    total = int(sum(stats.values()))
    return total

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

def find_problem(team):
    """ Find the type that is most effective against the team """
    weaknesses, resistances = team_summary(team)
    problem = []
    for attacker in chart:
        if weaknesses[attacker] > resistances[attacker]:
            problem.append((attacker, weaknesses[attacker] - resistances[attacker]))
    return problem

def problem_solver(pokemon_name, problems):
    """ How well a pokemon fixes the problem in the team """
    matchups = get_matchups(get_types(pokemon_name))
    score = 0
    for attacker, diff in problems:
        if matchups[attacker] < 1:
            score += diff
        elif matchups[attacker] > 1:
            score -= diff
    return score

def pokemon_suggester(team):
    """ Suggest a pokemon that would help cover issues in the current team """
    team = [name.strip().lower() for name in team]
    problems = find_problem(team)
    scores = []
    for pokemon_name in pokemon["name"]:
        if pokemon_name not in team:
            score = problem_solver(pokemon_name, problems)
            total_stats = get_total_stats(pokemon_name)
            scores.append((pokemon_name, score, total_stats))
    scores.sort(key=lambda x: (x[1], x[2]), reverse=True)
    return scores[:5]

if __name__ == "__main__":
    team = ["Pikachu", "Charizard", "Blastoise", "Venusaur", "Gengar", "Dragonite"]
    weaknesses, resistances = team_summary(team)

    print(find_problem(team))
    print(pokemon_suggester(team))