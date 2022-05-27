import json


def load_repos():
    with open("input/repos.json", encoding="UTF-8") as json_file:
        repos = json.load(json_file)

    return repos


def load_teams():
    with open("input/teams.json", encoding="UTF-8") as json_file:
        teams = json.load(json_file)

    return teams
