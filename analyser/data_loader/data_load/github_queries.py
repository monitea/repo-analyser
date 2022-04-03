from string import Template
from data_loader.data_models.repository import GitHubRepository
from gql import gql

repo_query = Template('repository(owner: "$owner", name: "$repo") {$part}')
pr_query_partial = Template(
    'repository(owner: "$owner", name: "$repo") {createdAt,pullRequests(first: 100 $after){totalCount,nodes {createdAt,number,permalink,state,merged,mergedAt,closed,closedAt,baseRefName,headRefName,author{login}}pageInfo{endCursor,hasNextPage}}}')
branch_query_partial = Template(
    'repository(owner: "$owner", name: "$repo") {createdAt,refs(first: 100, refPrefix: "refs/heads/", $after) {totalCount, pageInfo { endCursor,hasNextPage},nodes {name,target { ... on Commit { committedDate, author { user { login, name }}}}}}}')


def build_single_pr_query(repo: GitHubRepository, after=""):
    return gql('{' + pr_query_partial.substitute(owner=repo.owner, repo=repo.name, after=after) + '}')


def build_single_branch_query(repo: GitHubRepository, after=""):
    return gql('{' + branch_query_partial.substitute(owner=repo.owner, repo=repo.name, after=after) + '}')


def build_repo_query(repo: GitHubRepository):
    return gql('{' + repo_query.substitute(owner=repo.owner, repo=repo.name, part='createdAt') + '}')
