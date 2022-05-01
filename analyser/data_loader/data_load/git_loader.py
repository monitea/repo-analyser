from datetime import datetime, timedelta
import logging
from typing import List
from git import Repo
import shutil
import os
import sys
import re
from collections import Counter
from collections import OrderedDict
from pathlib import Path

repo_folder_base_path = "repos/"


def load_repo(repository_config: dict, repository: dict):
    token = repository_config.get('token')
    if token is None:
        token = ""

    grepo = __prepare_repo(
        protocol=repository_config.get('protocol'),
        server=repository_config.get('server'),
        owner=repository_config.get('owner'),
        name=repository_config.get('name'),
        token=token
    )
    repository["top_committers"] = __get_unique_committers(grepo, limit=10)
    repository["full_top_committers"] = __get_unique_committers(grepo)
    repository["top_committers_3m"] = __get_unique_committers(grepo, limit=10, after="3 months ago")
    repository["full_top_committers_3m"] = __get_unique_committers(grepo, after="3 months ago")
    repository["total_unique_committers"] = __get_unique_committers_number(grepo)
    repository["heatmap"] = __get_repository_heatmap(grepo,
                                                     ignore_list=repository_config["ignore_list"],
                                                     results=10
                                                     )
    repository["full_heatmap"] = __get_repository_heatmap(grepo,
                                                          ignore_list=repository_config["ignore_list"]
                                                          )

    repository["heatmap_3m"] = __get_repository_heatmap(grepo,
                                                        ignore_list=repository_config["ignore_list"],
                                                        after='3 months ago',
                                                        results=10
                                                        )
    repository["full_heatmap_3m"] = __get_repository_heatmap(grepo,
                                                             ignore_list=repository_config["ignore_list"],
                                                             after='3 months ago',
                                                             results=10
                                                             )

    unique_committers = []

    if repository["time_data"]["timestamps"]:
        for timestamp in repository["time_data"]["timestamps"]:
            when = datetime.fromtimestamp(timestamp, tz=None)
            committers_at = __get_unique_committers_number(repo=grepo, before=datetime.strftime(when, "%Y-%m-%d"),
                                                           after=(datetime.strftime(
                                                               when - timedelta(days=30), "%Y-%m-%d")))
            unique_committers.append(committers_at)

    if unique_committers:
        repository["time_data"]["unique_committers"] = unique_committers

    __repo_cleanup(repository_config.get('name'))


def __prepare_repo(protocol: str, server: str, owner: str, name: str, token: str = "") -> Repo:
    __repo_cleanup(name)

    Path(repo_folder_base_path).mkdir(parents=True, exist_ok=True)

    token_part = token + "@"

    repo_github_path = protocol + "://" + token_part + server + "/" + owner + "/" + name
    repo_folder_path = repo_folder_base_path + name

    try:
        Repo.clone_from(repo_github_path, repo_folder_path)
    except:
        sys.exit("Unable to clone repository from: " + repo_github_path)

    input_file = 'input/mailmap'
    mailmap_file = os.path.join(repo_folder_path, '.mailmap')

    if not os.path.isfile(mailmap_file):
        if os.path.isfile(input_file):
            shutil.copy('input/mailmap', repo_folder_path)
            copied_file = os.path.join(repo_folder_path, 'mailmap')
            os.rename(copied_file, mailmap_file)

    repo = Repo(repo_folder_path)

    return repo


def __get_unique_committers_number(repo: Repo, before="", after="") -> int:
    sorted_authors = __get_unique_committers(repo, before, after)

    return len(sorted_authors)


def __get_unique_committers(repo: Repo, before="", after="", limit=-1) -> List:
    repo_folder_path = repo.working_tree_dir
    mailmap_file = os.path.join(repo_folder_path, '.mailmap')
    params = []
    if os.path.isfile(mailmap_file):
        params.append(['--use-mailmap'])
    if before:
        params.append('--before=' + before)
    if after:
        params.append('--after=' + after)
    output = repo.git.log(params)
    split_data = output.split("\n")
    split_data = [entry.strip() for entry in split_data if "Author:" in entry]
    split_data = [entry.replace("Author: ", "") for entry in split_data]
    counted: Counter = Counter(split_data)
    sorted_authors = sorted(counted.items(), key=lambda x: x[1], reverse=True)
    sorted_authors = [{"name": key, "commits": value} for key, value in sorted_authors]

    if limit != -1:
        sorted_authors = sorted_authors[:limit]

    return sorted_authors


def __get_repository_heatmap(repo: Repo, before: str = "", after: str = "", ignore_list: List = [], results: int = -1):
    params = ['--name-only', '--no-merges', '--pretty=oneline']
    if before:
        params.append('--before=' + before)
    if after:
        params.append('--after=' + after)

    output = repo.git.log(params)
    split_data = output.split("\n")
    split_data = [entry.strip() for entry in split_data if entry]
    split_data = [entry for entry in split_data if not any(word in entry for word in ignore_list)]
    pattern = re.compile('\w{40}')
    split_data = [entry for entry in split_data if not pattern.match(entry)]

    counted: Counter = Counter(split_data)

    dd = OrderedDict(sorted(counted.items(), key=lambda x: x[1], reverse=True))

    data = [{"name": key, "value": value} for key, value in dd.items() if key]

    if results > 0:
        data = data[:results]

    return data


def __repo_cleanup(name):
    # TODO: check accesses
    logging.error("Cleanup called for: " + repo_folder_base_path + name)

