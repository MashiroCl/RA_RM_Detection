#sequence of commits
import os
import sys
import glob
import json

BEFORE_SQUASHED="before_squashed"

#create a folder to save information under current script path
def create_folder(folder):
    # folder= sys.argv[0]
    path=folder
    try:
        os.mkdir(path)
    except FileExistsError:
        print("Folder " + folder + "already exists, Directory recreated")
        os.system("rm -rf "+folder)

    return path

def read(file):
    f1=open(file)
    lines=f1.readlines()
    return lines

def git_merge(path,file_name="git_merge.txt"):
    os.system('git -C '+path+'/.git log --merges>'+file_name)
    return file_name


def git_log(path,file_name="git_log.txt"):
    os.system('git -C '+path+'/.git log>'+file_name)
    return file_name

def extract_commit(file_path):
    f1=open(file_path)
    lines=f1.readlines()
    commits=[]
    length=len(lines)
    for i,line in enumerate(lines):
        if "commit" in line:
            if i<length-1 and ("Merge: " in lines[i+1] or "Author: " in lines[i+1]):
                temp=line.split("commit ")[1]
                temp=temp.split("\n")[0]
                commits.append(temp)
    return commits

def extract_c_d(file_path):
    f1=open(file_path)
    lines=f1.readlines()
    c_d_lists=[]
    length=len(lines)
    c_d=[]
    for i,line in enumerate(lines):
        if "commit" in line:
            if i<length-1 and ("Merge: " in lines[i+1] or "Author: " in lines[i+1]):
                temp=line.split("commit ")[1]
                temp=temp.split("\n")[0]
                c_d.append(temp)
        if "Date:" in line:
            if i<length-1 and i-1>0 and "Author: " in lines[i-1]:
                temp=line.split("Date: ")[1]
                temp=temp.split("\n")[0]
                c_d.append(temp)
                c_d_lists.append(c_d)
                c_d=[]

    return c_d_lists


def RM(RM_path,repository,commits,output):
    for each in commits:
        command = RM_path + ' -c ' + repository + ' ' + each\
                  + ' -json ' +  output + "/" + each + ".json"
        os.system(command)


#strategy
def strategy(id,path):
    if id=="sequence":
        merge=extract_commit(git_merge(path))
        log=extract_commit(git_log(path))
        cc_lists=[]
        p_lists=[]
        j=0
        temp=[]
        for i in range(len(log)):
           if j<len(merge):
                if log[i]==merge[j]:
                    j=j+1
                    cc_lists.append(temp)
                    p_lists.append(log[i])
                    temp=[]
                else:
                    temp.append(log[i])

    elif id=="odd":
        pass

    return cc_lists,p_lists

def cc_cluster_info(path,commits):
    cc_cluster_info=path+"/cc_cluster_info.txt"
    f1=open(cc_cluster_info,"w")
    f1.write("#!/usr/bin/vi\n")
    for each in commits:
        f1.write(each)
    f1.close()
    return commits

def copy_auto_seq_editor(path):
    """
    :param path: path of the target repository
    :return:
    """
    auto_seq_editor = path + '/auto-seq-editor.rb'
    f2 = open(auto_seq_editor, 'w')
    f3 = open('./auto-seq-editor.rb')
    lines = f3.readlines()
    for each in lines:
        f2.write(each)
    f2.close()
    f3.close()
    os.system("chmod 777 "+path +"/auto-seq-editor.rb")

#squash the commits specified in the cc_cluster_info.txt
def squash(repository,commit_id):
    print("start squash")
    cc_cluster_info=repository+'/cc_cluster_info.txt'
    auto_seq_editor=repository+'/auto-seq-editor.rb'
    git_rebase='git rebase -i '+commit_id
    f1 = open(repository + "/squash.sh", 'w')
    command = "env "+"CC_CLUSTER_INFO="+cc_cluster_info+' '+'GIT_SEQUENCE_EDITOR='+auto_seq_editor+' '+git_rebase
    f1.write('cd '+repository+'\n'+command)
    f1.close()
    os.system('echo :wq| sh ' + repository + "/squash.sh")

def combine(output,compare_file):
    # commit_files = [output+"/" + x for x in os.listdir(output)]
    # create_folder(compare_file)
    # f2 = open(compare_file+"/before_squashed.txt", 'a+')
    # for each in commit_files:
    #     f1 = open(each)
    #     for each_line in f1:
    #         f2.write(each_line)
    #     f1.close()
    # return compare_file

    create_folder(compare_file)
    result=[]
    for f in glob.glob("*.json"):
        with open(f,"rb") as infile:
            result.append(json.load(infile))

    with open(compare_file+"/before_squashed.json","wb") as outfile:
        json.dump(result,outfile)
    return compare_file

# use date to find the squashed commit id
def find_after_squash(cc_commits,log1,log2):
    c_d_lists_1 = extract_c_d(log1)
    c_d_lists_2=extract_c_d(log2)

    temp=[]
    for each in c_d_lists_1:
        if each[0] in cc_commits:
            temp.append(each)

    for each in c_d_lists_2:
        if each[1]==temp[-1][1]:
            return each




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


def compare(before_squashed,after_squashed):
    before_squashed_refactorings = read_refactorings(before_squashed)
    after_squashed_refactorings = read_refactorings(after_squashed)
    difference = []
    for each in before_squashed_refactorings:
        flag = 0
        for each_2 in after_squashed_refactorings:
            if each == each_2:
                flag = 1
        if flag == 0:
            difference.append(each)
    print(len(before_squashed_refactorings))
    print(len(after_squashed_refactorings))
    print(len(difference))
    if (len(difference) == 0):
        print("there is no difference before and after squash")
    else:
        print("differences are ")
        for each in difference:
            print(each)


def process(id,path,RM_path,output,before_logF="before.txt",after_logF="after.txt",f_compare="compare_file"):
    #obtain git log before squash
    before_log=git_log(path,file_name=before_logF)
    #get before squashed commits
    cc_lists,p_lists=strategy(id, path)
    #write cc_cluster_info with commits before the 1st merge
    cc_commits=cc_cluster_info(path,cc_lists[0])
    #create output folder
    create_folder(output)
    #Refactoring Miner on commits in cc_cluster_info
    RM(RM_path,path,cc_commits,output)
    #Combine RM results into one txt
    compare_file=combine(output,f_compare)
    #copy auto-seq-editor.rb to the path
    copy_auto_seq_editor(path)
    #squash commits
    squash(path,p_lists[0])
    #obtain squashed git log
    squashed_log=git_log(path,file_name=after_logF)
    # #obtain squashed commit id
    # squashed_c_d=find_after_squash(cc_commits,before_log,squashed_log)
    # #RM on squashed commit
    # RM(RM_path,path,[squashed_c_d[0]],compare_file)
    # #Compare RM results
    # f1=compare_file+"/"+BEFORE_SQUASHED+".txt"
    # f2=compare_file+"/"+squashed_c_d[0]+".txt"
    # compare(f1,f2)




path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/refactoring-toy-example"
file_name="miao.txt"
merge_file="/Users/leichen/Code/pythonProject/For_file_compare/git_merge.txt"
log_file="/Users/leichen/Code/pythonProject/For_file_compare/git_log.txt"

RM_path="/Users/leichen/ResearchAssistant/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/RefactoringMiner"
# commits=extract_commit(merge_file)
# RM(RM_path,repository,commits,output)

path_jfinal="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal"
path_android_demos="/Users/leichen/ResearchAssistant/InteractiveRebase/data/android-demos"
output_jfinal="/Users/leichen/Code/pythonProject/For_file_compare/output_jfinal"
output_android_demos="/Users/leichen/Code/pythonProject/For_file_compare/output_android_demos"
output4="/Users/leichen/Code/pythonProject/For_file_compare/output4"
f_compare_jfinal="compare_file_jfinal"
f_compare_android_demos="compare_file_android_demos"
#id,path,RM_path,output,before_logF="before.txt",after_logF="after.txt",
#            ,f_compare="compare_file"
process("sequence",path_android_demos,RM_path,output_android_demos,f_compare_android_demos)


