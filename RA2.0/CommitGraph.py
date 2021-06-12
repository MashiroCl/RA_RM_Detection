import json
from Commit import Commit

class CommmitGraph():
    def __init__(self,commits:list):
        self.commits=commits
        self.num=len(commits)

    def whichCommit(self,commitID:str)->Commit:
        for each in self.commits:
            if each.commitID==commitID:
                return each

    def formGraph(self)->Commit:
        head=None
        tail=None
        for each in self.commits:
            if head==None:
                head=each
            for eachID in each.parentID:
                if len(eachID)>3:
                    each.setParent(self.whichCommit(eachID))
                    (self.whichCommit(eachID)).setChild(each)
                else :
                    tail=each
        return head

    def isConnected(self,c1,c2)->bool:
        flag=False
        for each in c1.parent:
            if  each==c2:
                flag=True
        for each in c1.child:
            if each==c2:
                flag=True
        return flag


    def SequenceCommit(self)->list:
        #start: child can be 1 or 2
        #middle: child must be 1
        cG=self.formGraph()
        cc_lists=[]
        p_lists=[]
        cc_list=[]
        p_list=[]

        for each in self.commits:
            if len(each.child)>2 or len(each.parentID)==2:
                if len(cc_list)!=0:
                    cc_lists.append(cc_list)
                    cc_list=[]
            else:
                if len(cc_list)==0:
                    cc_list.append(each)
                else:
                    if(self.isConnected(cc_list[-1],each)):
                        cc_list.append(each)
                    else:
                        cc_lists.append(cc_list)
                        cc_list = []
        return cc_lists

    def test(self,commit:Commit,cc_list:list,cc_lists:list):

        if ("4bf9a7f" in commit.commitID):
            print("!!!!!!!!")

        if (len(commit.parent) == 0):
                cc_list.append(commit)
                cc_lists.append(cc_list)
                return 1

        if len(commit.parent)==2:
            if len(cc_list) != 0:
                cc_lists.append(cc_list)
                cc_list = []
        elif len(commit.child)>2:
            if len(cc_list) != 0:
                cc_lists.append(cc_list)
                cc_list = []

            cc_list.append(commit)
        else:
                cc_list.append(commit)

        # if len(commit.child)>2 or len(commit.parent)==2:
        #         if len(cc_list)!=0:
        #             cc_lists.append(cc_list)
        #             cc_list=[]
        #         elif len(commit.parent)==1:
        #             cc_list.append(commit)
        # else:
        #     if len(cc_list) == 0:
        #         cc_list.append(commit)
        #     else:
        #         if (self.isConnected(cc_list[-1],commit)):
        #             cc_list.append(commit)
        #         else:
        #             cc_lists.append(cc_list)
        #             cc_list = []

        for each in commit.parent:
            return self.test(each,cc_list,cc_lists)

    def test2(self,commits:Commit,cc_list:list,cc_lists:list):

        for commit in commits:
            if (len(commit.parent) == 0):
                    cc_list.append(commit)
                    cc_lists.append(list(set(cc_list)))
                    return 1

            if len(commit.parent)==2:
                if len(cc_list) != 0:
                    cc_lists.append(cc_list)
                    cc_list = []
            elif len(commit.child)>2:
                if len(cc_list) != 0:
                    cc_lists.append(cc_list)
                    cc_list = []

                cc_list.append(commit)
            else:
                    cc_list.append(commit)

        return self.test2(commit.parent,cc_list,cc_lists)


def listSet(l):
    temp=[]
    for each in l:
        temp.append(list(set(each)))
    return temp

if __name__=="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal/test.json"
    with open(path) as f:
        data=json.loads("["+f.read()+"]")
    data=data[0]
    commits=[]
    for each in data:
        commits.append(Commit(each))

    cG=CommmitGraph(commits)
    # print(cG.whichCommit(cG.commits[0].parentID[0]).commitID)
    head=cG.formGraph()
    # print(cG.commits[cG.num-2].parent[0].commitID)
    # print(cG.whichCommit("d85b175db4ce63f102ff2071caa8655724aed537").child[0].commitID)
    # c=cG.SequenceCommit()

    cc_list = []
    cc_lists = []


    cG.test(head,cc_list,cc_lists)
    # temp=[head]
    # cG.test2(temp,cc_list,cc_lists)
    # cc_lists=listSet(cc_lists)

    # print(len(cG.whichCommit("a05da7f81debfa738c073c345d40815c5650da58").parent))
    # for each in cG.whichCommit("a05da7f81debfa738c073c345d40815c5650da58").parent:
    #     if each==None:
    #         print("!!!!!!!")

    # print(cG.isConnected(cG.whichCommit("125c4b00bf6a7d5f70dadaeb1992caf4f5682a24"),
    #                      cG.whichCommit("f2de6d8bcabdafe213dc7ba96de43d620cecaca1")))
    # print(cG.isConnected(cG.whichCommit("125c4b00bf6a7d5f70dadaeb1992caf4f5682a24"),None))
    # print(cc_lists)
    for each1 in cc_lists:
        print("_________________________")
        for each2 in each1:
            print(each2.commitID)
