import json

class Commit():
    def __init__(self,info:str):
        self.commitID=info["commit"]
        self.parentID=info["parent"].split(" ")
        self.suject=None
        self.commit_notes=info["commit_notes"]
        self.commiter=info["commiter"]
        self.isMerge=True if len(self.parentID)>1 else False
        self.parent=[]
        self.child=[]

    def setParent(self,pCommit):
        self.parent.append(pCommit)

    def setChinld(self,cCommit):
        self.child.append(cCommit)

if __name__ =="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal/test.json"
    with open(path) as f:
        data=json.loads("["+f.read()+"]")
    data=data[0]
    commits=[]
    for each in data:
        commits.append(Commit(each))
