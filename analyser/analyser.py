from data_loader.data_load import config_loader as cl, data_loader as dl, team_loader as tl
from datetime import date, datetime
import json

from data_loader.data_models.pr import PullRequest


def main():
    repositories_config = cl.load_repos()
    teams_config = cl.load_teams()
    repository_data = []

    for repository_config in repositories_config:
        repository = dl.load_repository(repository_config, teams_config)
        repository_data.append(repository)

    with open('output/repositories.json', 'w+') as outfile:
        json.dump(repository_data, outfile, default=json_serial)
        #  to deserialize use json.loads(json_string, object_hook=object_hook)

    team_data = []
    if teams_config:
        for team_config in teams_config:
            team = tl.load_team(team_config, repository_data)
            team_data.append(team)

        with open('output/teams.json', 'w+') as outfile:
            json.dump(team_data, outfile, default=json_serial)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, PullRequest):
        return {'__class__': 'PullRequest', '__dict__': obj.__dict__}
    else:
        return str(obj)


def object_hook(obj):
    if isinstance(obj, dict) and obj.get('__class__') == 'PullRequest':
        return PullRequest(**obj.get('__dict__'))
    return obj


if __name__ == "__main__":
    main()


