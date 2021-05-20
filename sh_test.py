import os

# os.system('sh /Users/leichen/Desktop/test.sh')
# os.system('/Users/leichen/ResearchAssistant/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/RefactoringMiner -h')

#Create a folder named RM under repository and a cc_cluster_info.txt
def create_work_space(repository):
    folder = os.path.exists(repository)
    if not folder:
        print("Not directory")
    else:
        os.makedirs(repository+"/RM")
        os.makedirs(repository + '/RM' + "/ready_to_squash")
    f1 = open(repository+"/RM"+"/cc_cluster_info.txt",'w')
    f1.close()
    f2 = open(repository + "/RM" + "/auto-seq-editor.rb", 'w')
    f3=open('./auto-seq-editor.rb')
    lines= f3.readlines()
    for each in lines:
        f2.write(each)
    f2.close()
    f3.close()
    f4 = open(repository + "/before_squash_gitlog.sh", 'w')
    f4.write('cd '+repository+'\n'+'git log >./RM/before_squash_gitlog.txt'+"\n"+"cd "+repository+"\RM\n"+"chmod 777"+" auto-seq-editor.rb")
    f4.close()
    os.system('sh '+ repository+"/before_squash_gitlog.sh")


repository="/Users/leichen/ResearchAssistant/InteractiveRebase/auto_test/refactoring-toy-example"
create_work_space(repository)
# command='git log'+' '+repository+' >' +repository+'/RM/before_gitlog.txt'
command='sh '+ repository+"/before_squash_gitlog.sh"
print(command)