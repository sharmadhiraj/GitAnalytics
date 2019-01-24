class Committer(object):
    name = ""
    email = ""
    commit_count = 0

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.commit_count = 1

    def increment_commit_count(self):
        self.commit_count += 1
