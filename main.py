#!/usr/bin/env python3

import os
import sys
import time
from dataclasses import dataclass, field

from git import Repo
from git.exc import InvalidGitRepositoryError, GitCommandError


@dataclass
class Committer:
    name: str
    email: str
    commit_count: int = field(default=1)

    def increment(self):
        self.commit_count += 1


def get_directory():
    return sys.argv[1] if len(sys.argv) > 1 else os.getcwd()


def setup_repository(directory):
    try:
        repo = Repo(directory)
        commits = list(repo.iter_commits())
        if not commits:
            raise GitCommandError("No commits", 1)
        print(f"Repository directory: {directory}")
        print(f"Total commits found: {len(commits)}")
        return repo, commits
    except (InvalidGitRepositoryError, GitCommandError) as e:
        print(f"Error: Not a valid git repository or no commits available ({e})")
        sys.exit(1)


def find_committer_index(commit, committers):
    return next((i for i, c in enumerate(committers) if c.email == commit.author.email), -1)


def gather_committers(commits):
    committers_by_email = {}
    for commit in commits:
        email = commit.author.email
        if email not in committers_by_email:
            committers_by_email[email] = Committer(commit.author.name, email)
        else:
            committers_by_email[email].increment()

    committers = list(committers_by_email.values())
    committers.sort(key=lambda c: c.commit_count, reverse=True)
    return committers


def display_committers(committers, total_commits):
    print("Commits by author:")
    for c in committers:
        percent = round(c.commit_count / total_commits * 100, 1)
        print(f"{c.commit_count} commits ({percent}%) from {c.name} <{c.email}>")


def gather_commit_spans(commits, current_time):
    spans = [0] * 5
    intervals = [3600, 86400, 604800, 2592000, 31104000]  # 1h,1d,1w,1m,1y
    for commit in commits:
        age = current_time - commit.authored_date
        for i, interval in enumerate(intervals):
            if age < interval:
                spans[i] += 1
    return spans


def display_commit_spans(spans, total_commits):
    labels = ["last 1 hour", "last 1 day", "last 1 week", "last 1 month", "last 1 year"]
    print("Commits by time:")
    for count, label in zip(spans, labels):
        percent = round(count / total_commits * 100, 1)
        print(f"{count} commits ({percent}%) in {label}")


def print_divider():
    print("=" * 90)


def main():
    current_time = int(time.time())
    directory = get_directory()

    print_divider()
    repo, commits = setup_repository(directory)
    total_commits = len(commits)
    print_divider()

    committers = gather_committers(commits)
    display_committers(committers, total_commits)
    print_divider()

    spans = gather_commit_spans(commits, current_time)
    display_commit_spans(spans, total_commits)
    print_divider()


if __name__ == "__main__":
    main()
