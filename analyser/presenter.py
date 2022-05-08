import json
import logging

from presenter.data_preparer import generate_repo_data, prepare_repo_html, generate_team_data


def main():

    with open('output/repositories.json', 'r') as outfile:
        repo_data = json.load(outfile)

    for repo in repo_data:
        generate_repo_data(repo)
        prepare_repo_html(repo["name"])

    try:
        with open('output/teams.json', 'r') as outfile:
            team_data = json.load(outfile)

        for team in team_data:
            generate_team_data(team, repo_data)
    except:
        logging.log("No file defining teams avialable, data will not be generated")


if __name__ == "__main__":
    main()
