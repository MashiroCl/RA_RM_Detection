import os
import sys

#Use refactoring miner to detect commits being squashed
def refactoring_miner_1(repository,refactoring_miner):
    """
    :param repository: current repository path
    :param refactoring_miner: path for refactoring_miner
    :return:
    """
    cc_cluster_info=repository+'/RM'+'/cc_cluster_info.txt'
    file= open(cc_cluster_info)
    lines=file.readlines()
    lines = [line[:-1] for line in lines]
    for i in range(len(lines)):
        if i==0:
            #jump through the line #!/usr/bin/vi
            pass
        else:
            command = refactoring_miner+' -c '+ repository+' '+lines[i]+' -json '+repository + "/RM/ready_to_squash"+"/"+lines[i]+".txt"
            print(command)
            os.system(command)


#squash the commits specified in the cc_cluster_info.txt
def squash(repository,commit_id):
    cc_cluster_info=repository+'/RM'+'/cc_cluster_info.txt'
    auto_seq_editor=repository+'/RM'+'/auto-seq-editor.rb'
    git_rebase='git rebase -i '+commit_id
    f1 = open(repository + "/squash.sh", 'w')
    command = "env "+"CC_CLUSTER_INFO="+cc_cluster_info+' '+'GIT_SEQUENCE_EDITOR='+auto_seq_editor+' '+git_rebase
    f1.write('cd '+repository+'\n'+command)
    f1.close()
    f2 = open(repository + "/after_squash_gitlog.sh", 'w')
    f2.write('cd ' + repository + '\n' + 'git log >./RM/after_squash_gitlog.txt')
    f2.close()
    os.system('echo :wq| sh ' + repository + "/squash.sh")
    os.system('sh '+repository+'/after_squash_gitlog.sh')

repository=sys.argv[1]
refactoring_miner=sys.argv[2]
commit_id=sys.argv[3]

refactoring_miner_1(repository,refactoring_miner)
squash(repository,commit_id)
