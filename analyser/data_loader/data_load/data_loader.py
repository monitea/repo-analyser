import datetime
from typing import Dict
from data_loader.data_load import git_loader as gl, github_loader as ghl


def load_repository(repository_config: dict, teams_config: dict) -> Dict:
    repository = {"owner": repository_config["owner"],
                  "name": repository_config["name"],
                  "ignore_list": repository_config["ignore_list"],
                  "generation_date": datetime.date.today().isoformat()
                  }

    ghl.load_repo(repository_config=repository_config, repository=repository, teams_config=teams_config)
    gl.load_repo(repository_config=repository_config, repository=repository, teams_config=teams_config)
    # logging.error(repository)

    return repository
