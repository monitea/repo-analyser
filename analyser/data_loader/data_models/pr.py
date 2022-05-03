import datetime
from enum import Enum


class PRStatus(str, Enum):
    OPEN = "OPEN"
    MERGED = "MERGED"
    CLOSED = "CLOSED"
    DRAFT = "DRAFT"


class PullRequest:
    state: str = None
    created_at: str = None
    closed: bool = None
    merged: bool = None
    closed_at: str = None
    merged_at: str = None
    permalink: str = None
    number: int = None
    baseRefName: str = None
    headRefName: str = None
    authorID: str = None

    def __init__(self, state, created_at, closed_at, merged, merged_at, permalink,
                 number, baseRefName, headRefName, closed, authorID):
        if isinstance(created_at, datetime.datetime):
            self.created_at = created_at.isoformat()
        if isinstance(closed_at, datetime.datetime):
            self.closed_at = closed_at.isoformat()
        self.permalink = permalink
        if isinstance(merged_at, datetime.datetime):
            self.merged_at = merged_at.isoformat()
        self.merged = merged
        self.number = number
        self.closed = closed
        self.baseRefName = baseRefName
        self.headRefName = headRefName
        self.authorID = authorID
        self.state = state

    def __repr__(self):
        return 'PR number={self.number} merged={self.merged} merged_at={self.merged_at} closed={self.closed} ' \
               'closed_at={self.closed_at} created_at={self.created_at} link={self.permalink} ' \
               'baseRefName={self.baseRefName} headRefName={self.headRefName} ' \
               'authorID={self.authorID}'.format(self=self)


def status_at(pull_request: PullRequest, when: datetime) -> str or None:
    if when is None:
        return None
    if datetime.datetime.fromisoformat(pull_request.created_at) < when:
        if (
                (pull_request.closed_at is None and pull_request.merged_at is None)
                or
                (pull_request.closed_at is not None and datetime.datetime.fromisoformat(pull_request.closed_at) >= when)
                or
                (pull_request.merged_at is not None and datetime.datetime.fromisoformat(pull_request.merged_at) >= when)
        ):
            return PRStatus.OPEN

        if pull_request.merged_at is not None and datetime.datetime.fromisoformat(pull_request.merged_at) < when:
            return PRStatus.MERGED

        if pull_request.closed_at is not None and datetime.datetime.fromisoformat(pull_request.closed_at) < when:
            return PRStatus.CLOSED

    return None


def age_at(pull_request: PullRequest, when: datetime):
    if when is None or datetime.datetime.fromisoformat(pull_request.created_at) > when:
        return None

    if status_at(pull_request, when) == PRStatus.MERGED:
        return datetime.datetime.fromisoformat(pull_request.merged_at) \
               - datetime.datetime.fromisoformat(pull_request.created_at)

    if status_at(pull_request, when) == PRStatus.CLOSED:
        return datetime.datetime.fromisoformat(pull_request.closed_at)\
               - datetime.datetime.fromisoformat(pull_request.created_at)

    return when - datetime.datetime.fromisoformat(pull_request.created_at)
