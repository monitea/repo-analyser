import datetime
from datetime import date
from enum import Enum


class PRStatus(str, Enum):
    OPEN = "OPEN"
    MERGED = "MERGED"
    CLOSED = "CLOSED"
    DRAFT = "DRAFT"


class PullRequest:
    state: str = None
    createdAt: date = None
    closed: bool = None
    merged: bool = None
    closedAt: date = None
    mergedAt: date = None
    permalink: str = None
    number: int = None
    baseRefName: str = None
    headRefName: str = None
    authorID: str = None

    def __init__(self, state, createdAt, closedAt, merged, mergedAt, permalink,
                 number, baseRefName, headRefName, closed, authorID):
        self.createdAt = createdAt
        self.closedAt = closedAt
        self.permalink = permalink
        self.mergedAt = mergedAt
        self.merged = merged
        self.number = number
        self.closed = closed
        self.baseRefName = baseRefName
        self.headRefName = headRefName
        self.authorID = authorID
        self.state = state

    def __repr__(self):
        return 'PR number={self.number} merged={self.merged} mergedAt={self.mergedAt} closed={self.closed} closedAt={' \
               'self.closedAt} createdAt={self.createdAt} link={self.permalink} baseRefName={self.baseRefName} ' \
               'headRefName={self.headRefName} authorID={self.authorID}'.format(self=self)


def status_at(pull_request: PullRequest, when: datetime) -> str or None:
    if when is None:
        return None
    if pull_request.createdAt < when:
        if (
                (pull_request.closedAt is None and pull_request.mergedAt is None) or
                (pull_request.closedAt is not None and pull_request.closedAt >= when) or
                (pull_request.mergedAt is not None and pull_request.mergedAt >= when)
        ):
            return PRStatus.OPEN

        if pull_request.mergedAt is not None and pull_request.mergedAt < when:
            return PRStatus.MERGED

        if pull_request.closedAt is not None and pull_request.closedAt < when:
            return PRStatus.CLOSED

    return None


def age_at(pull_request: PullRequest, when: datetime):
    if when is None or pull_request.createdAt > when:
        return None

    if status_at(pull_request, when) == PRStatus.MERGED:
        return pull_request.mergedAt - pull_request.createdAt

    if status_at(pull_request, when) == PRStatus.CLOSED:
        return pull_request.closedAt - pull_request.createdAt

    return when - pull_request.createdAt
