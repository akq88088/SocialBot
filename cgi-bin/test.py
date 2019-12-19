#!D:/Python/Python36/python.exe

import cgi, cgitb
import os
import pandas as pd
import numpy as np
import json
from module.QA_test import QA_test
from module import TextSummary
import glob
from module.NER import NER
from module.TextProcessor import TextProcessor
import time
import pymysql

print("Content-type:text/html") #必須
print('') #必須

parameter = cgi.FieldStorage()
text = '小明喜歡小美'
p_name = parameter.getvalue('p_name')
QA_test = QA_test('測試1')


iRun = 0
insert_id = 0
result_list = []
que_ans_dict = {}
try:
    df_result = QA_test.predict(text)
except:
    df_result = []
if len(df_result.columns) == 10:
    que_ans_dict = {}
    df_result = df_result.drop_duplicates(["輸入出題","輸入答案"])
    for i in range(len(df_result)):
        que_ans_dict.update({insert_id:[df_result["輸入出題"][i],df_result["輸入答案"][i]]})
        insert_id += 1
else:
    que_ans_dict.update({insert_id:["沒有產生問題","沒有產生答案"]})
print(json.dumps(que_ans_dict))
