#sequence of commits
import os
import sys
import glob
import json

BEFORE_SQUASHED="before_squashed"
RMSupportedREF="RMSupportedREF.txt"

def dictAdd(dictS,dict2)->dict:
    for each1 in dictS:
        for each2 in dict2:
            if each1.lower() == each2.lower():
                dictS[each1] += dict2[each2]
    return dictS
#create a folder to save information under current script path
def create_folder(folder):
    # folder= sys.argv[0]
    path=folder
    try:
        os.mkdir(path)
    except FileExistsError:
        print("Folder " + folder + "already exists, Directory recreated")
        os.system("rm -rf "+folder)
        os.mkdir(path)
    return path

def git_merge(path,file_name="git_merge.txt"):
    os.system('git -C '+path+'/.git log --merges>'+file_name)
    return file_name


def git_log(path,file_name="git_log.txt")->str:
    os.system('git -C '+path+'/.git log>'+file_name)
    return file_name

def count_commit(file_path):
    with open(file_path) as f:
        lines = f.readlines()
    length = len(lines)
    num=0
    for i, line in enumerate(lines):
        if "commit" in line:
            if i < length - 1 and ("Merge: " in lines[i + 1] or "Author: " in lines[i + 1]):
                num=num+1
    return num

def extract_commit(file_path)->list:
    with open(file_path) as f1:
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


def strategy(id,path,beforelog):
    if id=="sequence":
        merge=extract_commit(git_merge(path))
        log=extract_commit(beforelog)
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
    create_folder(compare_file)
    result=[]
    for f in glob.glob(output+"/"+"*.json"):
        with open(f,"r") as infile:
            result.append(json.load(infile))

    with open(compare_file+"/before_squashed.json","w") as outfile:
        json.dump(result,outfile)
    return compare_file

# use date to find the squashed commit id
def find_after_squash(cc_commits,log1,log2)->list:
    c_d_lists_1 = extract_c_d(log1)
    c_d_lists_2=extract_c_d(log2)

    temp=[]
    for each in c_d_lists_1:
        if each[0] in cc_commits:
            temp.append(each)

    for each in c_d_lists_2:
        try:
            if each[1]==temp[-1][1]:
                return each
        except IndexError:
            print("First commit contains merge")
            return None

# use type and description to determine it as an unique refactoirng
# def read_refactorings(file_path):
#     refactorings = []
#     file = open(file_path)
#
#     lines = file.readlines()
#     for i in range(len(lines)):
#         if '"type"' in lines[i]:
#             one_refactoring = []
#             one_refactoring.append(lines[i] + lines[i + 1])
#             refactorings.append(one_refactoring)
#
#     return refactorings


# def compare(f1_json,f2_json):
#     for each in (with open(f1_json))
#         flag = 0
#         for each_2 in after_squashed_refactorings:
#             if each == each_2:
#                 flag = 1
#         if flag == 0:
#             difference.append(each)
#     print(len(before_squashed_refactorings))
#     print(len(after_squashed_refactorings))
#     print(len(difference))
#     if (len(difference) == 0):
#         print("there is no difference before and after squash")
#     else:
#         print("differences are ")
#         for each in difference:
#             print(each)


def stat_analysis(f_json):
    with open(f_json,"r") as f1:
        list1=json.load(f1)
    dictS = RM_supported_type()
    #ref_num, num_of_each_type
    ref_num=0
    if isinstance(list1,list):
        pass
    else:
        list1=[list1]

    for each in list1:
        for each_r in each["commits"][0]["refactorings"]:
            ref_num=ref_num+1
            for eachD in dictS:
                if eachD.lower() == each_r['type'].lower():
                    dictS[eachD] = dictS[eachD] + 1
    return ref_num,dictS

def exclude_0_in_dict(dict):
    dict2={}
    for each in dict:
        if dict[each]!=0:
            dict2[each]=dict[each]
    return dict2


def RM_supported_type():
    dict={}
    with open(RMSupportedREF) as f:
       lines=f.readlines()
    for each in lines:
        dict[each.strip()]=0
    return dict

def process_one(path,RM_path,output,before_log,cc_list,p_list,after_logF="after.txt",f_compare="compare_file") -> list:
        # write cc_cluster_info with commits before the 1st merge
        cc_commits = cc_cluster_info(path, cc_list)
        # create output folder
        create_folder(output)
        # Refactoring Miner on commits in cc_cluster_info
        RM(RM_path, path, cc_commits, output)
        # Combine RM results into one txt
        compare_file=combine(output, f_compare)
        # squash commits
        squash(path, p_list)

        # obtain squashed git log
        squashed_log = git_log(path, file_name=after_logF)

        # obtain squashed commit id
        squashed_c_d = find_after_squash(cc_commits, before_log, squashed_log)

        ref_num_before=0
        dict1_temp={}
        ref_num_after=0
        dict2_temp={}

        if squashed_c_d is not None:
            # RM on squashed commit
            RM(RM_path, path, [squashed_c_d[0]], compare_file)
            f1=compare_file+"/"+BEFORE_SQUASHED+".json"
            f2 = compare_file + "/" + squashed_c_d[0] + ".json"
            ref_num_before,dict1_temp=stat_analysis(f1)
            ref_num_after, dict2_temp = stat_analysis(f2)

        return squashed_c_d[0],ref_num_before,ref_num_after,dict1_temp,dict2_temp

def findNextCommits(squashed_c,path,logF)->list:
    merge = extract_commit(git_merge(path))
    log = extract_commit(logF)
    cc_lists = []
    p_lists = []
    j = 0
    temp = []
    for i in range(len(log)):
        if j < len(merge):
            if log[i] == merge[j]:
                j = j + 1
                cc_lists.append(temp)
                p_lists.append(log[i])
                temp = []
            else:
                temp.append(log[i])
    print(cc_lists)
    for i in range(len(cc_lists)):
        if i+1<len(cc_lists):
            if cc_lists[i][0]==squashed_c:
                print("_________________________")
                print(cc_lists[i+1])
                print("ppppppppppppppp ", p_lists[i+1])
                return cc_lists[i+1],p_lists[i+1]
        else:
            return None,None

def process(id,path,RM_path,output,before_logF="before.txt",after_logF="after.txt",f_compare="compare_file"):
    #obtain git log before squash
    before_log=git_log(path,file_name=before_logF)
    #count commits num
    num_before=count_commit(before_log)


    #get before squashed commits
    cc_lists,p_lists=strategy(id, path,before_log)
    for i in range(len(cc_lists)):
        print("cc_lists: ", cc_lists[i])
        print("p_lists: ", p_lists[i])


    # copy auto-seq-editor.rb to the path
    copy_auto_seq_editor(path)

    ref_num_before = 0
    ref_num_after = 0
    dict_before = RM_supported_type()
    dict_after = RM_supported_type()

    merge = extract_commit(git_merge(path))
    log = extract_commit(before_log)

    if id=="sequence":
        squashed_c=None
        cc_list=[]
        p_list=[]
        while True:
            #first time
            if squashed_c==None:
                cc_list=cc_lists[0]
                p_list=p_lists[0]
                squashed_c, num1, num2, dict1, dict2 = process_one(path, RM_path, output, before_log,
                                                                   cc_list, p_list, after_logF, f_compare)
                ref_num_before=ref_num_before+num1
                ref_num_after = ref_num_after+num2
                dictAdd(dict_before,dict1)
                dictAdd(dict_after, dict2)

            else:
                #find commits after squashed_c and merge
                logF = git_log(path, file_name=before_logF)
                cc_list,p_list=findNextCommits(squashed_c,path,logF)
                if cc_list==p_list==None:
                    break
                else:
                    squashed_c, num1, num2, dict1, dict2 = process_one(path, RM_path, output, before_log,
                                                                   cc_list, p_list, after_logF, f_compare)
                    ref_num_before = ref_num_before + num1
                    ref_num_after = ref_num_after + num2
                    dictAdd(dict_before, dict1)
                    dictAdd(dict_after, dict2)


        # for i in range(len(cc_lists)):
        #     if len(cc_lists[i])!=0:
        #         num1,num2,dict1,dict2=process_one(path,RM_path,output,before_log,cc_lists[i],p_lists[i],after_logF,f_compare)
        #         ref_num_before=ref_num_before+num1
        #         ref_num_after = ref_num_after+num2
        #         dictAdd(dict_before,dict1)
        #         dictAdd(dict_after, dict2)

    # count commits num
    num_after = count_commit(after_logF)
    print("Fine grained",num_before,"commits in total: ", "Total ",ref_num_before," detected, ",exclude_0_in_dict(dict_before))
    print("Coarese-grained",num_after,"commits in total: ", "Total ",ref_num_after," detected, ",exclude_0_in_dict(dict_after))

         # for i in range(len(cc_lists)):
         #    #write cc_cluster_info with commits before the 1st merge
         #    cc_commits=cc_cluster_info(path,cc_lists[i])
         #    #create output folder
         #    create_folder(output)
         #    #Refactoring Miner on commits in cc_cluster_info
         #    RM(RM_path,path,cc_commits,output)
         #    #Combine RM results into one txt
         #    compare_file=combine(output,f_compare)
         #
         #    #squash commits
         #    squash(path,p_lists[i])
         #    # #write cc_cluster_info with commits before the 1st merge
         #    # cc_commits=cc_cluster_info(path,cc_lists[0])
         #    # #create output folder
         #    # create_folder(output)
         #    # #Refactoring Miner on commits in cc_cluster_info
         #    # RM(RM_path,path,cc_commits,output)
         #    # #Combine RM results into one txt
         #    # compare_file=combine(output,f_compare)
         #    #
         #    # #squash commits
         #    # squash(path,p_lists[0])
         # # obtain squashed git log
         # squashed_log=git_log(path,file_name=after_logF)
         # #count commits num
         # num_after=count_commit(after_logF)
         # #obtain squashed commit id
         # squashed_c_d=find_after_squash(cc_commits,before_log,squashed_log)

    # if squashed_c_d is not None:
    #     #RM on squashed commit
    #     RM(RM_path,path,[squashed_c_d[0]],compare_file)
    #     # #Compare RM results
    #     f1=compare_file+"/"+BEFORE_SQUASHED+".json"
    #     f2=compare_file+"/"+squashed_c_d[0]+".json"
    #     # compare(f1,f2)
    #     ref_num_before,dict1_temp=stat_analysis(f1)
    #     ref_num_after, dict2_temp = stat_analysis(f2)
    #     print("Fine grained",num_before,"commits in total: ", "Total ",ref_num_before," detected, ",exclude_0_in_dict(dict1_temp))
    #     print("Coarese-grained",num_after,"commits in total: ", "Total ",ref_num_after," detected, ",exclude_0_in_dict(dict2_temp))



path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/refactoring-toy-example"
file_name="miao.txt"
merge_file="/Users/leichen/Code/pythonProject/For_file_compare/git_merge.txt"
log_file="/Users/leichen/Code/pythonProject/For_file_compare/git_log.txt"

RM_path="/Users/leichen/ResearchAssistant/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/RefactoringMiner"

path_refactoring_toy="/Users/leichen/ResearchAssistant/InteractiveRebase/data/refactoring-toy-example"
path_jfinal="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal"
path_android_demos="/Users/leichen/ResearchAssistant/InteractiveRebase/data/android-demos"
path_mbassador="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"

output_jfinal="/Users/leichen/Code/pythonProject/For_file_compare/output_jfinal"
output_android_demos="/Users/leichen/Code/pythonProject/For_file_compare/output_android_demos"
output_refactoring_toy="/Users/leichen/Code/pythonProject/For_file_compare/refactoring-toy-example"
output_mbassador="/Users/leichen/Code/pythonProject/For_file_compare/mbassador"



f_compare_jfinal="compare_file_jfinal"
f_compare_android_demos="compare_file_android_demos"
f_compare_refactoring_toy="compare_file_refactoring_toy"
f_compare_mbassador="compare_file_mbassador"


#id,path,RM_path,output,before_logF="before.txt",after_logF="after.txt",
#            ,f_compare="compare_file"
# process(id="sequence",path=path_refactoring_toy,RM_path=RM_path,output=output_refactoring_toy,f_compare=f_compare_refactoring_toy)
# process(id="sequence",path=path_jfinal,RM_path=RM_path,output=output_jfinal,f_compare=f_compare_jfinal)
process(id="sequence",path=path_mbassador,RM_path=RM_path,output=output_mbassador,f_compare=f_compare_mbassador)


