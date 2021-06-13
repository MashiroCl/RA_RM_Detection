import os
class RefactoringMiner:
    def __init__(self):
        self.RMPath=None

    def setRMPath(self,path):
        self.RMPath=path

    def detect(self,repository,commits:list,output):
        for each in commits:
            command = self.RMPath + ' -c ' + repository + ' ' + each \
                      + ' -json ' + output + "/" + each + ".json"
            os.system(command)
