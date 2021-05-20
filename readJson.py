import json

# test_dict = {'bigberg': [7600, {1: [['iPhone', 6300], ['Bike', 800], ['shirt', 300]]}]}
# print(test_dict)
# print(type(test_dict))
# #dumps 将数据转换成字符串
# json_str = json.dumps(test_dict)
# print(json_str)
# print(type(json_str))
#

with open("/Users/leichen/Code/pythonProject/For_file_compare/RA2.0/compare_file_refactorint_toy/bf26de10dfc3a9deff362e5189279086476d3012.json",'r') as load_f:
    load_dict = json.load(load_f)
    print(load_dict)

print(load_dict['commits'][0]["repository"])