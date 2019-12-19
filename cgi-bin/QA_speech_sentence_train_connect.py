#!D:/Python/Python36/python.exe
#!C:/ProgramData/Anaconda3/python.exe

import cgi, cgitb
import os
import pandas as pd
import numpy as np
import json
from module.QA_train import QA_train

def json2df(data):
    data = json.loads(data)
    result = []
    for i in range(0,len(data)):
        try:
            data[i] = data[i][:2]
            data_type = data[i][0].lstrip().rstrip()
            # with open("C:\\Users\\student\\Desktop\\json_test.txt",'a') as fout:    
            #     fout.write(data_type + '\n')
            #     fout.write('---\n')
        except:
            continue
        if data_type == "刪除":
            data_type = "remove"
        elif data_type == "新增":
            data_type = "insert"
        elif data_type == "修改":
            data_type = "change"
        elif data_type == "上傳":
            data_type = "upload"
        else:
            pass
        data[i][0] = data_type
        # with open("C:\\Users\\student\\Desktop\\json_test.txt",'a') as fout:
        #     for row in data[i]:
        #         fout.write(str(row) + '\n')
        result.append(data[i])
    df = pd.DataFrame(np.array(result))
    # df["owner"] = owner
    df.columns = ["datatype","ID"]
    # with open("C:\\Users\\student\\Desktop\\json_test.txt",'a') as fout:
    #     fout.write(str(df.head()))
    return df

parameter = cgi.FieldStorage()
data = parameter.getvalue('data')
owner = parameter.getvalue('owner')
p_name = parameter.getvalue('p_name')
df = json2df(data)
QA_train = QA_train(owner,p_name)
QA_train.speech_sentence_train_main(df)
print("Content-type:texspeech_train_maint/html") #必須
print('') #必須
print('QA train finish')