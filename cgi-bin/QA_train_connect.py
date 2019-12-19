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
            data[i] = data[i][:8]
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
    df.columns = ["datatype","ID","原文規則","原文出題規則","原文出題規則答案","原文斷詞","原文出題","原文出題答案"]
    # with open("C:\\Users\\student\\Desktop\\json_test.txt",'a') as fout:
    #     fout.write(str(df.head()))
    return df

# QA_train = QA_train()
# df = QA_train.get_training_data()
# data_dir = 'C:\\Users\\student\\desktop\\test.csv'
# df.to_csv(data_dir,index=0,encoding='utf_8_sig')
parameter = cgi.FieldStorage()
data = parameter.getvalue('data')
owner = parameter.getvalue('owner')
p_name = parameter.getvalue('p_name')
# owner = parameter.getvalue('owner')
df = json2df(data)
# temp = [["insert",0,"X","X","X","X","X","X","X"]]
# temp = [["remove",0,"X","X","X","X","X","X","X"]]
# temp = [["change",0,"X","X","1","2","X","X","X"]]
# df = pd.DataFrame(np.array(temp))
# df.columns = ["datatype","ID","owner","原文規則","原文出題規則","原文出題規則答案","原文斷詞","原文出題","原文出題答案"]
# for i in range(len(df)):
#     temp = df.iloc[i,:]
#     for ele in temp:
#         print(type(ele))
# print(len(df))
QA_train = QA_train(owner,p_name)
QA_train.QA_train_main(df)
# data_dir = 'D:\\dektop\\work_data_backup_0923_2256\\rule_all.csv'
# data_dir = 'D:\\dektop\\QA_test_demo\\cgi-bin\\module\\QA_data\\insert_remove_change_test.csv'
# df = pd.read_csv(data_dir)

# QA_train.QA_train_main(df)
print("Content-type:text/html") #必須
print('') #必須
print('QA train finish')