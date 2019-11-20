#!D:/Python/Python36/python.exe
#!C:/ProgramData/Anaconda3/python.exe
import cgi, cgitb
import os
import pandas as pd
import numpy as np
import json
from module.QA_train import QA_train

def text2df(data):
    sentence_list = data.split('\n')
    result = []
    for i in range(1,len(sentence_list)):
        temp = sentence_list[i].split(',')
        for j in range(len(temp)):
            temp[j] = temp[j].lstrip().rstrip()
            temp[j] = temp[j].replace('\r','')
            temp[j] = temp[j].replace('\n','')
        if len(temp) != 2:
            continue
        if temp[0] == '' or temp[1] == '' or temp[0] != temp[0] or temp[1] != temp[1]:
            continue
        result.append(temp)
    result = pd.DataFrame(np.array(result))
    # result['owner'] = owner
    result.columns = ["字詞","實體"]
    return result
        
parameter = cgi.FieldStorage()
data = parameter.getvalue('data')
owner = parameter.getvalue('owner')
p_name = parameter.getvalue('p_name')
text = text2df(data)
QA_train = QA_train(owner,p_name)
QA_train.insert_remain_transfer_dict(text)
#轉成dict回傳
print("Content-type:text/html") #必須
print('') #必須
print('QA upload finish')