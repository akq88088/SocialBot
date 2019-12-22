#!D:/Python/Python36/python.exe
#!C:/ProgramData/Anaconda3/python.exe

import cgi, cgitb
import os
import pandas as pd
import numpy as np
import json
from module.QA_train import QA_train
parameter = cgi.FieldStorage()
data = parameter.getvalue('data')
p_name = parameter.getvalue('p_name')
result_dict = {}
QA_train = QA_train("",p_name)
article_remain,que_remain,flag_que_remain_dict,boson_flag = QA_train.get_rule_check_data()
result_dict.update({"article_remain":article_remain,"que_remain":que_remain,"flag_que_remain_dict":flag_que_remain_dict,"boson_flag":boson_flag})
# result_dict.update({"article_remain":article_remain})
# result_dict.update({"article_remain":"a"})
data_dir = 'C:\\Users\\student\\Desktop\\test.txt'
print("Content-type:text/html") #必須
print('') #必須
print(json.dumps(result_dict))
# print("finish")