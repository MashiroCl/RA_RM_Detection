"""
1.create a json file read json file
2.find cc_lists and p_lists
3.RM on current all commits (merge excluded)
4.squash
5.RM on remaining all commits (merge excluded)
"""
from jsonUtils import JsonUtils
from CommitGraph import CommitGraph
from CommitGraph import printCClists
import os

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

#write commits into cc_cluster_info.txt
def cc_cluster_info(path,commits)->list:
    cc_cluster_info=path+"/cc_cluster_info.txt"
    f1=open(cc_cluster_info,"w")
    f1.write("#!/usr/bin/vi\n")
    for each in commits:
        f1.write(each)
    f1.close()
    return commits

#Copy auto_seq_editor to the repository
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

#combine RM result of being squashed commit json files into one
def combine(output,compare_file):
    create_folder(compare_file)
    result=[]
    for f in glob.glob(output+"/"+"*.json"):
        with open(f,"r") as infile:
            result.append(json.load(infile))

    with open(compare_file+"/before_squashed.json","w") as outfile:
        json.dump(result,outfile)
    return compare_file

repoPath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal"
if __name__=="__main__":
    #create a json file read json file
    jF=JsonUtils()
    jF.setRepoPath(repoPath)
    jF.createJson()
    commits=jF.jsonToCommit()

    #create commit graph
    cG = CommitGraph(commits)
    head = cG.formGraph()

    #Extract cc_lists
    cc_lists = cG.getCClist()
    printCClists(cc_lists)

    #p_list[i]=cc_lists[i][-1].parent[0]

