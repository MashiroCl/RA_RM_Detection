from read_refactoirngs_from_commit_file import read_refactorings

before_squashed="/Users/leichen/JAVA/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/MPS_RM/result/squash_2/all_to_one.txt"
after_squashed="/Users/leichen/JAVA/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/MPS_RM/result/squash_2/squashed/9a131b8b868c3c600c2882a4c8a481f07f306b8a.txt"
before_squashed_refactorings=read_refactorings(before_squashed)
after_squashed_refactorings=read_refactorings(after_squashed)

difference=[]

for each in before_squashed_refactorings:
    flag=0
    for each_2 in after_squashed_refactorings:
        if each == each_2:
            flag=1
    if flag==0:
        difference.append(each)
print(len(before_squashed_refactorings))
print(len(after_squashed_refactorings))
print(len(difference))