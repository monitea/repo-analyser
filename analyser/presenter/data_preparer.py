import datetime
import logging
import json
import shutil
from pathlib import Path
import random


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

        if "open_prs" in info:
            datasets.append(
                {
                    "data": info["open_prs"],
                    "label": name + ": Open PRs",
                    "borderColor": info["color"],
                    "fill": "false"
                }
            )
        if "open_prs_long_living" in info:
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
    start_date_iso = min([repo["created_at"] for repo in team["repositories"]])
    when = datetime.datetime.fromisoformat(start_date_iso)
    days = []

    while True:
        days.append(datetime.datetime.strftime(when, "%Y-%m-%d"))
        when += datetime.timedelta(days=1)
        if when > datetime.datetime.now():
            break

    time_data = {
        "days": days,
        "repos": []
    }

    for repo in team["repositories"]:
        repo_data = {"name": repo["name"]}
        open_pulls_long_living = []
        open_pulls = []
        for day in days:
            if day in repo["time_data"]["days"]:
                open_pulls_long_index = repo["time_data"]["days"].index(day)
                if "open_prs" in repo:
                    open_pulls_long_living.append(repo["open_prs_long_living"][open_pulls_long_index])
                    open_pulls_index = repo["time_data"]["days"].index(day)
                    open_pulls.append(
                        repo["open_prs"][open_pulls_index])
            else:
                open_pulls_long_living.append(0)
                open_pulls.append(0)
        if open_pulls_long_living:
            repo_data["open_pulls_long_living"] = open_pulls_long_living

        if open_pulls:
            repo_data["open_pulls"] = open_pulls
        time_data["repos"].append(repo_data)

    team_data = team.copy()
    del(team_data["first_created_date"])
    for repo in team_data["repositories"]:
        del(repo["time_data"])
        if "open_prs_long_living" in repo:
            del(repo["open_prs_long_living"])
        if "open_prs" in repo:
            del(repo["open_prs"])

    Path("reports/html/teams/" + team_data["name"].lower() + "/data").mkdir(parents=True, exist_ok=True)

    with open('reports/html/teams/' + team_data["name"].lower() + '/data/team.js', 'w+') as outfile:
        outfile.write('var teamdata = ')
    with open('reports/html/teams/' + team_data["name"].lower() + '/data/team.js', 'a') as outfile:
        json.dump(team_data, outfile)

    datasets = []
    r = lambda: random.randint(0, 255)
    for repo in time_data["repos"]:
        if "open_pulls_long_living" in repo:
            datasets.append(
                {
                    "data": repo["open_pulls_long_living"],
                    "label": repo["name"] + ": Open PRs to long living branches",
                    "borderColor": '#%02X%02X%02X' % (r(),r(),r()),
                    "fill": "false"
                }
            )
        if "open_pulls" in repo:
            datasets.append(
                {
                    "data": repo["open_pulls"],
                    "label": repo["name"] + ": Open PRs",
                    "borderColor": '#%02X%02X%02X' % (r(), r(), r()),
                    "fill": "false"
                }
            )

    team_time_data = {
            "labels": time_data["days"],
            "datasets": datasets
        }

    with open('reports/html/teams/' + team_data["name"].lower() + '/data/team_time.js', 'w+') as outfile:
        outfile.write('var timedata = ')
    with open('reports/html/teams/' + team_data["name"].lower() + '/data/team_time.js', 'a') as outfile:
        json.dump(team_time_data, outfile)

    shutil.copy('presenter/resources/team/index.html', 'reports/html/teams/' + team_data["name"] + "/")
    shutil.copy('presenter/resources/team/script.js', 'reports/html/teams/' + team_data["name"] + "/")
    shutil.copy('presenter/resources/team/Chart.2.8.0.bundle.min.js', 'reports/html/teams/' + team_data["name"] + "/")
    shutil.copy('presenter/resources/team/style.css', 'reports/html/teams/' + team_data["name"] + "/")
