import datetime
from datetime import datetime, timedelta


def load_team(team_config, repository_data):
    team_name = team_config["name"]
    team = {
        "name": team_name,
        "color": team_config["color"],
        "members": team_config["members"]
    }

    first_created_date = min([repo["created_at"] for repo in repository_data])
    team["first_created_date"] = first_created_date
    members_committer_names = [member["name"] + " <" + member["email"] + ">" for member in team["members"]]
    member_ids = [member["login"] for member in team["members"]]

    days = []
    when = first_created_date
    while True:
        days.append(datetime.strftime(when, "%Y-%m-%d"))
        when += timedelta(days=1)
        if when > datetime.now():
            break

    team_repos = []
    for repo in repository_data:
        repo_name = repo["name"]
        team_repo = {
            "name": repo_name,
            "owner": repo["owner"],
            "created_at": repo["created_at"],
            "time_data": {}
        }
        top_committers = [entry for entry in repo["full_top_committers"]
                          if entry["name"] in members_committer_names]
        team_repo["top_committers"] = top_committers[0:10]
        top_committers_3m = [entry for entry in repo["full_top_committers_3m"]
                             if entry["name"] in members_committer_names]
        team_repo["top_committers_3m"] = top_committers_3m[0:10]
        stale_branches = [branch for branch in repo["stale_branches"] if branch["lastAuthorId"] in member_ids]
        team_repo["stale_branches"] = stale_branches
        if "open_prs" in repo["teams"][team_name]:
            team_repo["open_prs"] = repo["teams"][team_name]["open_prs"]
        if "open_prs_long_living" in repo["teams"][team_name]:
            team_repo["open_prs_long_living"] = repo["teams"][team_name]["open_prs_long_living"]
        team_repo["time_data"]["days"] = repo["time_data"]["days"]
        team_repo["time_data"]["timestamps"] = repo["time_data"]["timestamps"]
        team_repos.append(team_repo)

    team["repositories"] = team_repos

    #
    # for day in days:
    #     for repo in repository_data:
    #
    #
    #         open_prs_at = repo.open_prs_at(datetime.datetime.strptime(day, "%Y-%m-%d"))
    #         value = len([pr for pr in open_prs_at if pr.authorID in team_member_logins]) \
    #             if open_prs_at is not None else None
    #         team_stat[repo_name].append(value)

    return team


# team contributions
# team hotspots
