# Read commits under file_path and write them into one txt file
import os
import glob

# file_path = "/Users/leichen/JAVA/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/MPS_RM/result/squash_2/"
# file_squashed_path = file_path + "squashed.txt"


def read_write_file(path, f):
    commit_files = [path + x for x in os.listdir(path)]
    f2 = open(f, 'a+')
    for idx, folder in enumerate(commit_files):
        for im in glob.glob(folder + '/*.txt'):
            f1 = open(im, 'r')
            for eachLine in f1:
                f2.write(eachLine)
                # f2.write(' '+'\n')
            f1.close()


# read_write_file(file_path, file_squashed_path)