import json
import logging

from presenter.data_preparer import generate_repo_data, prepare_repo_html


def main():

    with open('output/repositories.json', 'r') as outfile:
        data = json.load(outfile)

    for repo in data:
        generate_repo_data(repo)
        prepare_repo_html(repo["name"])


if __name__ == "__main__":
    main()
