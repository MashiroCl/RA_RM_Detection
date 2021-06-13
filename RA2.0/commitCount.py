def commitCount(path):
    with open(path) as f:
        lines=f.readlines()
    num=0
    for each in lines:
        if "commit " in each:
            num+=1
    return num

path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal"
num=commitCount(path+"/log.txt")
print(num)