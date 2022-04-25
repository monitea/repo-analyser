
def load_team(team_config, repository_data):
    team = {
        "name": team_config["name"],
        "color": team_config["color"],
        "members": team_config["members"]
    }

    first_created_date = min([repo["created_at"] for repo in repository_data])
    team["first_created_date"] = first_created_date
    members_committer_names = [member["name"] + " <" + member["email"] + ">" for member in team["members"]]
    member_ids = [member["login"] for member in team["members"]]
    team_repos = []
    for repo in repository_data:
        team_repo = {
            "name": repo["name"],
            "owner": repo["owner"]
        }
        top_committers = [entry for entry in repo["full_top_committers"]
                          if entry["name"] in members_committer_names]
        team_repo["top_committers"] = top_committers[0:10]
        top_committers_3m = [entry for entry in repo["full_top_committers_3m"]
                             if entry["name"] in members_committer_names]
        team_repo["top_committers_3m"] = top_committers_3m[0:10]
        stale_branches = [branch for branch in repo["stale_branches"] if branch["lastAuthorId"] in member_ids]
        team_repo["stale_branches"] = stale_branches
        team_repos.append(team_repo)

    team["repositories"] = team_repos

    return team


# team contributions
# team hotspots
