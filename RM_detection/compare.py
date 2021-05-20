import os
import sys

# Read commits under file_path and write them into one txt file
def read_write_file(repository):
    path=repository+"/RM/ready_to_squash/"
    commit_files = [path + x for x in os.listdir(path)]
    print(commit_files)
    f2 = open(repository+"/RM/before_squashed.txt", 'a+')
    for each in commit_files:
        f1 = open(each)
        for each_line in f1:
            f2.write(each_line)
        f1.close()

# use type and description to determine it as an unique refactoirng
def read_refactorings(file_path):
    refactorings = []
    file = open(file_path)

    lines = file.readlines()
    for i in range(len(lines)):
        if '"type"' in lines[i]:
            one_refactoring = []
            one_refactoring.append(lines[i] + lines[i + 1])
            refactorings.append(one_refactoring)

    return refactorings

#Use refactoring miner to detect squashed commits
def refactoring_miner_2(repository,refactoring_miner,squashed_commit):
    """
    :param repository: current repository path
    :param refactoring_miner: path for refactoring_miner
    squashed_commit:
    :return:
    """
    command = refactoring_miner + ' -c ' + repository + ' ' + squashed_commit +' -json '+repository+'/RM/after_squashed.txt'
    os.system(command)


def compare(repository):
    # Read commits under file_path and write them into one txt file
    read_write_file(repository)

    before_squashed=repository+"/RM/before_squashed.txt"
    after_squashed=repository+"/RM/after_squashed.txt"

    before_squashed_refactorings=read_refactorings(before_squashed)
    after_squashed_refactorings=read_refactorings(after_squashed)

    difference = []

    for each in before_squashed_refactorings:
        flag = 0
        for each_2 in after_squashed_refactorings:
            if each == each_2:
                flag = 1
        if flag == 0:
            difference.append(each)

    f1=open(repository+"/RM/compare_result.txt",'w')

    print("number of refactoring operations detected before squash ",len(before_squashed_refactorings))
    print("number of refactoring operations detected after squash ",len(after_squashed_refactorings))
    print("number of different operations detected ",len(difference))
    if (len(difference)==0):
        f1.write("there is no difference before and after squash")
    else:
        f1.write("different results are \n")
        for each in difference:
            f1.write(str(each[0]))

    f1.close()
repository=sys.argv[1]
refactoring_miner=sys.argv[2]
squashed_commit=sys.argv[3]

refactoring_miner_2(repository,refactoring_miner,squashed_commit)
compare(repository)