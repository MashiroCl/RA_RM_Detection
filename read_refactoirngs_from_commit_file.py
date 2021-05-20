# use type and description to determine it as an unique refactoirng

def read_refactorings(file_path):
    refactorings = []
    file = open(file_path)

    lines = file.readlines()
    for i in range(len(lines)):
        if '"type"' in lines[i]:
            # print(lines[i]+lines[i+1])
            one_refactoring = []
            one_refactoring.append(lines[i] + lines[i + 1])
            refactorings.append(one_refactoring)

    return refactorings


# txt_file_path = "/Users/leichen/JAVA/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/MPS_RM/result/squash_2/d96ba95cfc6999691cf63b7412602b4f09284e9a.txt"
# refactorings = read_refactorings(txt_file_path)
# print(refactorings[2])
# print(len(refactorings))