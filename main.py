import time

from git import Repo
from committer import Committer
import sys

repo = None
commits = []
committer_list = []
commits_in_span = [0, 0, 0, 0, 0]
commits_count = 0
current_time = int(time.time())
git_dir = "/Users/dhirajsharma/Project/GitAnalytics"


def get_committer_index(commit):
    return next((i for i, item in enumerate(committer_list) if item.email == commit.author.email), -1)


def format_commit_count(count):
    return str(count) + " commits (" + str(
        round(count / commits_count * 100, 1)) + "%)"


def divider():
    print("=========================================================================================")


def set_up_repo():
    global repo, commits, commits_count

    try:
        repo = Repo(git_dir)
        commits = list(repo.iter_commits())
    except:
        print("Not valid git repo or no commits available.")
        sys.exit(1)

    commits_count = len(commits)
    print("Total commits : " + str(commits_count))


def filter_commits_for_committer():
    for commit in commits:
        index = get_committer_index(commit)
        if index == -1:
            committer_list.append(Committer(commit.author.name, commit.author.email))
        else:
            committer_list[index].increment_commit_count()

    committer_list.sort(key=lambda x: x.commit_count, reverse=True)


def log_committer_stats():
    print("Commits by author")
    for committer in committer_list:
        print(
            format_commit_count(committer.commit_count) +
            " from " +
            committer.name +
            "(" + committer.email + ")"
        )


def filter_commits_for_spans():
    for commit in commits:
        commit_ago = current_time - commit.authored_date
        if commit_ago < 3600:
            commits_in_span[0] += 1
        if commit_ago < 86400:
            commits_in_span[1] += 1
        if commit_ago < 604800:
            commits_in_span[2] += 1
        if commit_ago < 2592000:
            commits_in_span[3] += 1
        if commit_ago < 31104000:
            commits_in_span[4] += 1


def log_spans_stats():
    print("Commits by time")
    print(format_commit_count(commits_in_span[0]) + " in last one hour")
    print(format_commit_count(commits_in_span[1]) + " in last one day")
    print(format_commit_count(commits_in_span[2]) + " in last one week")
    print(format_commit_count(commits_in_span[3]) + " in last one month")
    print(format_commit_count(commits_in_span[4]) + " in last one year")


def main():
    divider()
    set_up_repo()
    divider()
    filter_commits_for_committer()
    log_committer_stats()
    divider()
    filter_commits_for_spans()
    log_spans_stats()
    divider()


main()
