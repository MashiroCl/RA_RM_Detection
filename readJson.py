import json

# test_dict = {'bigberg': [7600, {1: [['iPhone', 6300], ['Bike', 800], ['shirt', 300]]}]}
# print(test_dict)
# print(type(test_dict))
# #dumps 将数据转换成字符串
# json_str = json.dumps(test_dict)
# print(json_str)
# print(type(json_str))
#

path="/Users/leichen/Code/pythonProject/For_file_compare/RA2.0/compare_file_refactoring_toy/before_squashed.json"
# with open("/Users/leichen/Code/pythonProject/For_file_compare/RA2.0/compare_file_refactorint_toy/bf26de10dfc3a9deff362e5189279086476d3012.json",'r') as load_f:
with open(path) as load_f:
    load_dict = json.load(load_f)
    # print(type(load_dict))
    # print(isinstance(load_dict,list))




RMSupportedREF="RMSupportedREF.txt"

def RM_supported_type():
    dict={}
    with open(RMSupportedREF) as f:
       lines=f.readlines()
    for each in lines:
        dict[each.strip()]=0
    return dict


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
    # print(dictS)


    for each in list1:
        for each_r in each["commits"][0]["refactorings"]:
            print("each_r['type']",each_r['type'])
            ref_num=ref_num+1;
            for eachD in dictS:
                print(eachD)
                if eachD.lower()=="Move And Rename Method".lower():
                    print("YES")

                if eachD.lower() == each_r['type'].lower():
                    dictS[eachD] = dictS[eachD] + 1
                    print(eachD)



    return ref_num,dictS

def exclude_0_in_dict(dict):
    dict2={}
    for each in dict:
        if dict[each]!=0:
            dict2[each]=dict[each]
    return dict2



a="/Users/leichen/Code/pythonProject/For_file_compare/RA2.0/compare_file_refactoring_toy/40087b18a5ac2880b4f231e1f278663ae2c1424f.json"
b="/Users/leichen/Code/pythonProject/For_file_compare/RA2.0/compare_file_refactoring_toy/before_squashed.json"
ref_num,dict=stat_analysis(a)
print(ref_num)
print(exclude_0_in_dict(dict))