import logging
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
import aiohttp
from data_loader.data_load import github_queries as queries
from data_loader.data_models.repository import GitHubRepository
from data_loader.data_models.pr import PullRequest, age_at
from datetime import timedelta, datetime


def load_repo(repository_config: dict, repository: dict, teams_config: dict):
    ghrepo = GitHubRepository(name=repository_config["name"], owner=repository_config["owner"])
    logging.debug(repository_config)

    client = __prepare_client(
        protocol=repository_config.get('protocol'),
        server=repository_config.get('api'),
        token=repository_config.get('token')
    )

    __query_for_repo_data(client=client, repo=ghrepo)
    __query_for_prs(client=client, repo=ghrepo)
    __query_for_branches(client=client, repo=ghrepo)
    repository["created_at"] = ghrepo.createdAt
    repository["prs"] = ghrepo.pulls
    repository["branches_number"] = len(ghrepo.branches)
    repository["branches_list"] = ghrepo.branches
    longest = str(ghrepo.oldest_open_pr_age_at(datetime.now()))
    repository["oldest_pr"] = longest
    total_prs = ghrepo.prs_number_at(datetime.now())
    repository["total_prs"] = total_prs
    stale_period = repository_config.get('stale_branch_after')
    if stale_period:
        repository["stale_branches"] = ghrepo.get_stale_branches(stale_period)
    else:
        repository["stale_branches"] = ghrepo.get_stale_branches()
    repository["stale_branches_number"] = len(repository["stale_branches"])
    open_prs_long_living = ghrepo.open_prs_long_living_number_at(repository_config.get('long_living_branches'),
                                                                 datetime.now())
    repository["open_prs_long_living_now"] = open_prs_long_living
    repository["median_pr_lifetime"] = str(ghrepo.median_open_pr_age_at(datetime.now()))
    repository["total_open_prs_now"] = ghrepo.open_prs_number_at(datetime.now())
    if repository["total_open_prs_now"] > 0:
        oldest_pr = ghrepo.oldest_open_pr_at(datetime.now())
        repository["oldest_pr_link"] = oldest_pr.permalink
        repository["oldest_pr_age"] = " " + str(age_at(oldest_pr, datetime.now()).days) + " days"
    else:
        repository["oldest_pr_link"] = None
        repository["oldest_pr_age"] = None

    days = []
    timestamps = []
    open_pulls = []
    open_pulls_long_living = []
    medians = []
    merged_last_week = []

    repository["time_data"] = {}
    repository["teams"] = {}

    when = repository["created_at"]

    team_logins = {}
    if teams_config:
        for team in teams_config:
            team_logins[team["name"]] = [member["login"] for member in team["members"]]
            repository["teams"][team["name"]] = {
                "open_prs": [],
                "open_prs_long_living": [],
                "medians": [],
                "color": team["color"]
            }

    while True:
        days.append(datetime.strftime(when, "%Y-%m-%d"))
        timestamps.append(datetime.timestamp(when))

        open_prs_number = ghrepo.open_prs_number_at(when)
        open_pulls.append(open_prs_number)

        open_prs = ghrepo.open_prs_at(when)
        open_prs_long_living = ghrepo.open_prs_long_living_at(
            repository_config.get('long_living_branches'),
            when
        )

        open_prs_long_living_number = ghrepo.open_prs_long_living_number_at(
            repository_config.get('long_living_branches'),
            when
        )

        open_pulls_long_living.append(open_prs_long_living_number)

        median_at = ghrepo.median_open_pr_age_at(when)
        medians.append(median_at)

        last_week_at = ghrepo.sliding_window_merged_prs_number_at(when, 7)
        merged_last_week.append(last_week_at)

        if teams_config:
            for team in teams_config:
                team_prs = [pr for pr in open_prs if pr.authorID in team_logins[team["name"]]]
                repository["teams"][team["name"]]["open_prs"].append(len(team_prs))
                team_prs_long_living = [pr for pr in open_prs_long_living if pr.authorID in team_logins[team["name"]]]
                repository["teams"][team["name"]]["open_prs_long_living"].append(len(team_prs_long_living))
                team_median = ghrepo.median_open_pr_age_at(when, team_logins[team["name"]])
                repository["teams"][team["name"]]["medians"].append(team_median)

        when += timedelta(days=1)
        if when > datetime.now():
            break

    if teams_config:
        for team in teams_config:
            if not [number for number in repository["teams"][team["name"]]["open_prs"] if number > 0]:
                del(repository["teams"][team["name"]]["open_prs"])
                del(repository["teams"][team["name"]]["open_prs_long_living"])

    medians = [median.total_seconds() / 3600 / 24 for median in medians]

    if teams_config:
        for team in teams_config:
            team_medians = repository["teams"][team["name"]]["medians"]
            repository["teams"][team["name"]]["medians"] = [median.total_seconds() / 3600 / 24
                                                            for median in team_medians]

    repository["time_data"]["days"] = days
    repository["time_data"]["open_pulls"] = open_pulls
    repository["time_data"]["open_pulls_long_living"] = open_pulls_long_living
    repository["time_data"]["merged_last_week"] = merged_last_week
    repository["time_data"]["medians"] = medians
    repository["time_data"]["timestamps"] = timestamps


def __prepare_client(protocol: str, server: str, token: str = ""):
    logging.debug("token")
    logging.debug(token)
    github_domain: str = protocol + "://" + server
    jar = aiohttp.CookieJar()
    headers = {'Accept': 'application/json'}
    authorization = "Bearer " + token
    headers['Authorization'] = authorization

    logging.debug("headers")
    logging.debug(headers)
    transport = AIOHTTPTransport(url=github_domain, client_session_args={'cookie_jar': jar}, headers=headers)

    client = Client(transport=transport)
    return client


def __query_for_repo_data(client: Client, repo: GitHubRepository):
    query = queries.build_repo_query(repo)
    result = client.execute(query)
    logging.debug(result)
    created_str = result['repository']['createdAt']
    repo.createdAt = datetime.strptime(created_str, "%Y-%m-%dT%H:%M:%SZ")
    logging.debug(repo)
    logging.debug(repo.createdAt)


def __query_for_prs(client: Client, repo: GitHubRepository):
    after = ""
    while True:
        pr_query_single = queries.build_single_pr_query(repo, after)
        result = client.execute(pr_query_single)
        __parse_prs(repo, result)

        if result['repository']['pullRequests']['pageInfo']['hasNextPage']:
            after = ',after:"' + result['repository']['pullRequests']['pageInfo']['endCursor'] + '"'
        else:
            break


def __parse_prs(repo: GitHubRepository, json_data):
    for node in json_data['repository']['pullRequests']['nodes']:

        created_at = None
        if node['createdAt']:
            created_at = datetime.strptime(node['createdAt'], "%Y-%m-%dT%H:%M:%SZ")

        closed_at = None
        if node['closedAt']:
            closed_at = datetime.strptime(node['closedAt'], "%Y-%m-%dT%H:%M:%SZ")

        merged_at = None
        if node['mergedAt']:
            merged_at = datetime.strptime(node['mergedAt'], "%Y-%m-%dT%H:%M:%SZ")

        author_id = "Unknown"
        if node["author"]:
            author_id = node['author']['login']

        pr = PullRequest(
            created_at=created_at,
            closed=node['closed'],
            closed_at=closed_at,
            merged=node['merged'],
            merged_at=merged_at,
            number=node['number'],
            permalink=node['permalink'],
            state=node['state'],
            baseRefName=node['baseRefName'],
            headRefName=node['headRefName'],
            authorID=author_id
        )
        repo.pulls.append(pr)


def __query_for_branches(client: Client, repo: GitHubRepository):
    after = ""
    repo.branches.clear()
    while True:
        branch_query_single = queries.build_single_branch_query(repo, after)
        branches = client.execute(branch_query_single)
        __parse_branches(repo, branches)

        if branches['repository']['refs']['pageInfo']['hasNextPage']:
            after = ',after:"' + branches['repository']['refs']['pageInfo']['endCursor'] + '"'
        else:
            break


def __parse_branches(repo: GitHubRepository, json_data):
    for node in json_data['repository']['refs']['nodes']:
        branch_name = node['name']
        branch_last_commit = node['target']['committedDate']
        branch_last_commit = datetime.strptime(branch_last_commit, "%Y-%m-%dT%H:%M:%SZ")
        branch_last_commit = datetime.strftime(branch_last_commit, "%Y-%m-%d")
        author = node['target']['author']['user']
        if author:
            branch_last_author = author['name']
            branch_last_author_id = author['login']
        else:
            branch_last_author = "Unknown"
            branch_last_author_id = "Unknown"

        repo.branches.append(
            {
                "name": branch_name,
                "lastCommit": branch_last_commit,
                "lastAuthor": branch_last_author,
                "lastAuthorId": branch_last_author_id
            }
        )
