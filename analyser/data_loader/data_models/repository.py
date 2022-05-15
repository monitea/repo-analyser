import datetime
from datetime import timedelta
from typing import List
from data_loader.data_models.pr import PullRequest, status_at, age_at, PRStatus
import numpy as np


class GitHubRepository:
    name: str = None
    owner: str = None
    createdAt: datetime = None
    sliding_window_length = 7
    pulls: List[PullRequest] = []
    branches: List[str] = []

    def __repr__(self):
        return 'GitHubRepository: name={self.name} owner={self.owner}'.format(self=self)

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.pulls = []
        self.branches = []

    def prs_at(self, when: datetime) -> List or None:
        if when < self.createdAt:
            return None
        return [pr for pr in self.pulls if datetime.datetime.fromisoformat(pr.created_at) < when]

    def prs_long_living_at(self, long_living: List, when: datetime) -> List or None:
        if when < self.createdAt:
            return None
        prs = self.prs_at(when)
        prs = [pull for pull in prs if
               pull.baseRefName in long_living]
        return prs

    def prs_number_at(self, when: datetime) -> int or None:
        if when < self.createdAt:
            return None
        return len(self.prs_at(when))

    def open_prs_at(self, when: datetime) -> List or None:
        if when < self.createdAt:
            return None
        open_prs = self.prs_at(when)
        open_prs = [pr for pr in open_prs if (status_at(pr, when) == PRStatus.OPEN)]
        return open_prs

    def open_prs_long_living_at(self, long_living: List, when: datetime) -> List or None:
        if when < self.createdAt:
            return None
        open_prs = self.prs_long_living_at(long_living, when)
        open_prs = [pr for pr in open_prs if (status_at(pr, when) == PRStatus.OPEN)]
        return open_prs

    def open_prs_number_at(self, when: datetime) -> int or None:
        if when < self.createdAt:
            return None
        open_prs = self.open_prs_at(when)
        return len(open_prs)

    def open_prs_long_living_number_at(self, long_living: List, when: datetime) -> int or None:
        if when < self.createdAt:
            return None
        open_prs = self.open_prs_long_living_at(long_living, when)
        return len(open_prs)

    def open_prs_over_age(self, age: timedelta) -> List or None:
        open_prs = self.open_prs_at(datetime.datetime.now())
        older = [pr for pr in open_prs if
                 (datetime.datetime.now() - datetime.datetime.fromisoformat(pr.created_at) > age)]
        return older

    def open_prs_number_over_age(self, age: timedelta) -> int or None:
        old_prs = self.open_prs_over_age(age)
        return len(old_prs)

    def discarded_prs_at(self, when: datetime) -> List or None:
        if when < self.createdAt:
            return None
        pulls = self.prs_at(when)
        discarded = [pr for pr in pulls if (status_at(pr, when) == PRStatus.CLOSED) and pr.merged_at is None]
        return discarded

    def discarded_prs_number_at(self, when: datetime) -> int or None:
        if when < self.createdAt:
            return None
        discarded_prs = self.discarded_prs_at(when)
        return len(discarded_prs)

    def merged_prs_at(self, when: datetime) -> List or None:
        if when < self.createdAt:
            return None
        pulls = self.prs_at(when)
        merged = [pr for pr in pulls if (status_at(pr, when) == PRStatus.MERGED)]
        return merged

    def merged_prs_number_at(self, when: datetime) -> int or None:
        if when < self.createdAt:
            return None
        merged_prs = self.merged_prs_at(when)
        return len(merged_prs)

    def sliding_window_merged_prs_number_at(self, when: datetime, window: int) -> int or None:
        if when < self.createdAt:
            return None
        sliding_window_merges = self.merged_prs_at(when)
        sliding_window_merges = [pr for pr in sliding_window_merges
                                 if (when - datetime.datetime.fromisoformat(pr.merged_at))
                                 <= timedelta(days=window if window else self.sliding_window_length)]
        return len(sliding_window_merges)

    def median_pr_age_at(self, when: datetime) -> timedelta or None:
        if when < self.createdAt:
            return None
        pulls = self.prs_at(when)
        ages = [age_at(pr, when) for pr in pulls]
        if len(ages) == 0:
            return timedelta(hours=0)
        if len(ages) == 1:
            return ages[0]
        return np.median(ages)

    def median_open_pr_age_at(self, when: datetime, users: list = None) -> timedelta or None:
        if when < self.createdAt:
            return None
        pulls = self.open_prs_at(when)
        if users:
            pulls = [pull for pull in pulls if pull.authorID in users]
        ages = [age_at(pr, when) for pr in pulls]
        if len(ages) == 0:
            return timedelta(hours=0)
        if len(ages) == 1:
            return ages[0]
        return np.median(ages)

    def oldest_open_pr_age_at(self, when: datetime) -> timedelta or None:
        if when < self.createdAt:
            return None
        pulls = self.open_prs_at(when)
        ages = [age_at(pr, when) for pr in pulls if status_at(pr, when) == PRStatus.OPEN]
        if ages:
            return max(ages)
        return timedelta(hours=0)

    def oldest_open_pr_at(self, when: datetime) -> PullRequest or None:
        if when < self.createdAt:
            return None
        pulls = self.open_prs_at(when)
        if pulls:
            max_age = self.oldest_open_pr_age_at(when)
            pulls = [pr for pr in pulls if age_at(pr, when) == max_age]
            return pulls[0]
        return None

    def max_pr_age_at(self, when: datetime) -> timedelta or None:
        if when < self.createdAt:
            return None
        ages = [age_at(pr, when) for pr in self.pulls if status_at(pr, when) is not None]
        if ages:
            return max(ages)
        else:
            return timedelta(hours=0)

    def min_pr_age_at(self, when: datetime) -> timedelta or None:
        if when < self.createdAt:
            return None
        ages = [age_at(pr, when) for pr in self.pulls if status_at(pr, when) is not None]
        if ages:
            return min(ages)
        else:
            return timedelta(hours=0)

    def get_stale_branches(self, stale_days: int = 30):

        def is_stale(input_data):
            now = datetime.datetime.now()
            last_commit = datetime.datetime.strptime(input_data["lastCommit"], "%Y-%m-%d")
            if (now - last_commit).days > stale_days:
                return True

            return False

        stale_branches = [branch for branch in self.branches if is_stale(branch)]

        return stale_branches
