from git import Repo
from committer import Committer
import sys

repo = None
commits = []
committer_list = []
commits_in_span = [0, 0, 0, 0]
commits_count = 0
# git_dir = "/home/dhirajsharma/Drive/Arson/Projects/Python/GitAnalytics/"
git_dir = "/home/dhirajsharma/Drive/SmartMobe/Projects/Android/4service-android/"


def get_committer_index(commit):
    return next((i for i, item in enumerate(committer_list) if item.email == commit.author.email), -1)


def main():
    global repo, commits, commits_count

    try:
        repo = Repo(git_dir)
        commits = list(repo.iter_commits())
    except:
        print("Not valid git repo or no commits available.")
        sys.exit(1)

    commits_count = len(commits)
    print("Total commits : " + str(commits_count))
    filter_commits_for_committer()


def filter_commits_for_committer():
    for commit in commits:
        index = get_committer_index(commit)
        if index == -1:
            committer_list.append(Committer(commit.author.name, commit.author.email))
        else:
            committer_list[index].increment_commit_count()

    committer_list.sort(key=lambda x: x.commit_count, reverse=True)
    log_committer_stats()


def log_committer_stats():
    for committer in committer_list:
        print(
            str(committer.commit_count) +
            " commits (" +
            str(round(committer.commit_count / commits_count * 100, 1)) +
            "%) from " +
            committer.name +
            "(" + committer.email + ")"
        )


main()
