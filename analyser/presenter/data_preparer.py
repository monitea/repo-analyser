import logging
import json
import shutil
from pathlib import Path


def generate_repo_data(repo):
    repo_data = {}
    repo_data.update(repo)
    del repo_data["time_data"]

    Path("reports/html/git/" + repo_data["name"] + "/data").mkdir(parents=True, exist_ok=True)

    with open('reports/html/git/' + repo_data["name"] + '/data/repo-data.js', 'w+') as outfile:
        outfile.write('var repodata = ')
    with open('reports/html/git/' + repo_data["name"] + '/data/repo-data.js', 'a') as outfile:
        json.dump(repo_data, outfile)

    time_data = {}
    time_data.update(repo["time_data"])

    pr_data = {
            "labels": time_data["days"],
            "datasets": [
                {
                    "data": time_data["open_pulls"],
                    "label": "Open PRs",
                    "borderColor": "#a83289",
                    "fill": "false"
                },
                {
                    "data": time_data["open_pulls_long_living"],
                    "label": "Open PRs to long living branches",
                    "borderColor": "#000dff",
                    "fill": "false"
                },
                {
                    "data": time_data["unique_committers"],
                    "label": "Unique committers last month",
                    "borderColor": "#88C647",
                    "fill": "false"
                }
            ]
        }

    with open('reports/html/git/' + repo_data["name"] + '/data/pr-trends.js', 'w+') as outfile:
        outfile.write('var prdata = ')

    with open('reports/html/git/' + repo_data["name"] + '/data/pr-trends.js', 'a') as outfile:
        json.dump(pr_data, outfile)

    merge_data = {
        "labels": time_data["days"],
        "datasets": [
            {
                "data": time_data["medians"],
                "label": "Median open PR lifetime in days",
                "borderColor": "#A428F0",
                "fill": "false"
            },
            {
                "data": time_data["merged_last_week"],
                "label": "PRs merges last week (sliding window)",
                "borderColor": "#000000",
                "fill": "false"
            }
        ]
    }
    with open('reports/html/git/' + repo_data["name"] + '/data/merge-trends.js', 'w+') as outfile:
        outfile.write('var mergedata = ')

    with open('reports/html/git/' + repo_data["name"] + '/data/merge-trends.js', 'a') as outfile:
        json.dump(merge_data, outfile)

    # team data
    datasets = []
    for name, info in repo_data["teams"].items():
        datasets.append(
            {
                "data": info["open_prs"],
                "label": name + ": Open PRs",
                "borderColor": info["color"],
                "fill": "false"
            }
        )
        datasets.append(
            {
                "data": info["open_prs_long_living"],
                "label": name + ": Open PRs to long living branches",
                "borderColor": info["color"],
                "fill": "false"
            }
        )

    team_data = {
            "labels": time_data["days"],
            "datasets": datasets
        }

    with open('reports/html/git/' + repo_data["name"] + '/data/teams.js', 'w+') as outfile:
        outfile.write('var teamdata = ')

    with open('reports/html/git/' + repo_data["name"] + '/data/teams.js', 'a') as outfile:
        json.dump(team_data, outfile)


def prepare_repo_html(name: str):
    shutil.copy('presenter/resources/git/index.html', 'reports/html/git/' + name + "/")
    shutil.copy('presenter/resources/git/script.js', 'reports/html/git/' + name + "/")
    shutil.copy('presenter/resources/git/style.css', 'reports/html/git/' + name + "/")
    shutil.copy('presenter/resources/git/Chart.2.8.0.bundle.min.js', 'reports/html/git/' + name + "/")


def generate_team_data(team: dict, repos: dict):
    repo_data = repos.copy()

    team_data = {}
    team_data.update(team)

    for repo in team_data["repositories"]:
        repo["days"] = [repod["time_data"]["days"] for repod in repo_data if repo["name"]==repod["name"]]

    time_data = team_data["repositories"].copy()
    del(team_data["repositories"])


    Path("reports/html/teams/" + team_data["name"].lower() + "/data").mkdir(parents=True, exist_ok=True)

    with open('reports/html/teams/' + team_data["name"].lower() + '/data/team.js', 'w+') as outfile:
        outfile.write('var teamdata = ')
    with open('reports/html/teams/' + team_data["name"].lower() + '/data/team.js', 'a') as outfile:
        json.dump(team_data, outfile)


    #
    # pr_data = {
    #         "labels": time_data["days"],
    #         "datasets": [
    #             {
    #                 "data": time_data["open_pulls"],
    #                 "label": "Open PRs",
    #                 "borderColor": "#a83289",
    #                 "fill": "false"
    #             },
    #             {
    #                 "data": time_data["open_pulls_long_living"],
    #                 "label": "Open PRs to long living branches",
    #                 "borderColor": "#000dff",
    #                 "fill": "false"
    #             },
    #             {
    #                 "data": time_data["unique_committers"],
    #                 "label": "Unique committers last month",
    #                 "borderColor": "#88C647",
    #                 "fill": "false"
    #             }
    #         ]
    #     }
    #
    # with open('reports/html/git/' + repo_data["name"] + '/data/pr-trends.js', 'w+') as outfile:
    #     outfile.write('var prdata = ')
    #
    # with open('reports/html/git/' + repo_data["name"] + '/data/pr-trends.js', 'a') as outfile:
    #     json.dump(pr_data, outfile)
