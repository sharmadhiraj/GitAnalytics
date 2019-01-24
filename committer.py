class Committer(object):
    name = ""
    email=""
    count = 0

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.count = 1

    def addCommit(self):
    	self.count=self.count+1