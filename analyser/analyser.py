from data_loader.data_load import config_loader as cl, data_loader as dl
import json


def main():
    repositories_config = cl.load_repos()
    repository_data = []

    for repository_config in repositories_config:
        repository = dl.load_repository(repository_config)
        repository_data.append(repository)
        with open('output/repositories.json', 'w+') as outfile:
            json.dump(repository_data, outfile, default=str)
        # with open('output/' + repository_config["name"] + '.json', 'w+') as outfile:
        #     json.dump(repository, outfile, default=str)


if __name__ == "__main__":
    main()
