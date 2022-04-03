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


def prepare_repo_html(name: str):
    shutil.copy('presenter/resources/git/index.html', 'reports/html/git/' + name + "/")
    shutil.copy('presenter/resources/git/script.js', 'reports/html/git/' + name + "/")
    shutil.copy('presenter/resources/git/nav.js', 'reports/html/git/' + name + "/")
    shutil.copy('presenter/resources/git/style.css', 'reports/html/git/' + name + "/")
    shutil.copy('presenter/resources/git/Chart.2.8.0.bundle.min.js', 'reports/html/git/' + name + "/")

