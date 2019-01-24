from git import Repo
from committer import Committer
import sys

git_dir = "/home/dhirajsharma/Drive/Arson/Projects/Python/GitAnalytics/"

try:
	repo = Repo(git_dir)
	commits = repo.iter_commits()
except:
	print("Not valid git repo or no commits available.")
	sys.exit(1)

committer_list = []
for commit in commits:
	index = next((i for i, item in enumerate(committer_list) if item.email == commit.author.email), -1)
	if(index==-1):
		committer_list.append(Committer(commit.author.name,commit.author.email))
	else:
		committer_list[index].addCommit()

committer_list.sort(key=lambda x: x.count, reverse=True)
for committer in committer_list:
	print(str(committer.count)+" commits from "+committer.name+"("+committer.email+")")

