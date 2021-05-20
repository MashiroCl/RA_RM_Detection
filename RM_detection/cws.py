"""
create work space like following

|-repository/
|---before_squash_gitlog.sh      to produce gitlog
|---RM/
|-----cc_cluster_info.txt
|-----before_squash_gitlog.txt
|-----auto-seq-editor.rb
|-----ready_to_squash/

"""

import os
import sys


#Create a folder named RM under repository and a cc_cluster_info.txt
def create_work_space():
    repository=sys.argv[1]
    folder = os.path.exists(repository)
    if not folder:
        print("Not directory")
    else:
        if not (os.path.exists(repository+"/RM") and os.path.isdir(repository+"/RM")):
            os.makedirs(repository+"/RM")
        if not (repository + '/RM' + "/ready_to_squash") and os.path.isdir(repository + '/RM' + "/ready_to_squash"):
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
    f4.write('cd '+repository+'\n'+'git log >./RM/before_squash_gitlog.txt'+"\n"+"cd "+repository+"/RM\n"+"chmod 777"+" auto-seq-editor.rb")
    f4.close()
    os.system('sh '+ repository+"/before_squash_gitlog.sh")

create_work_space()