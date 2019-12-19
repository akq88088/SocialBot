#!D:/Python/Python36/python.exe
#!C:/ProgramData/Anaconda3/python.exe
import cgi, cgitb
import sys,codecs
import os
import pandas as pd
import numpy as np
import json
from module.QA_test import QA_test
from module import TextSummary
import glob
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

def getSummary(text,algorithm="textsim",percentage=0.4):
    algoritm_dic = {"textsim": TextSummary.TextSim_TextSum(),
                    "textrank": TextSummary.TextRank_TextSum(),
                    "textmap": TextSummary.TRMap_TextSum()}

    Summary = algoritm_dic[algorithm]
    return " ".join(Summary.summary(text, compression_ratio=percentage))

parameter = cgi.FieldStorage()
text = parameter.getvalue('text')
p_name = parameter.getvalue('p_name')
# p_name = "測試1"
# p_name = "tt"
# owner = parameter.getvalue('owner')
QA_test = QA_test(p_name)
iRun = 0
insert_id = 0
result_list = []
# que_ans_dict = {}
que_ans_list = []
try:
    df_result = QA_test.predict(text)
    if len(df_result.columns) == 10:
        df_result = df_result.drop_duplicates(["輸入出題","輸入答案"])
        for i in range(len(df_result)):
            que_ans_list.append([df_result["輸入出題"][i],df_result["輸入答案"][i]])
except:
    df_result = []
if len(que_ans_list) < 1:
    que_ans_list.append(["沒有產生問題","沒有產生答案"])
    
print("Content-type:text/html") #必須
print('') #必須
print(que_ans_list)
