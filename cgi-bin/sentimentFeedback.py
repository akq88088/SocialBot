#!D:/Python/Python36/python.exe
#!C:/Users/mcu/AppData/Local/Programs/Python/Python36/python.exe
#!C:/ProgramData/Anaconda3/python.exe
#!D:/Anaconda3/python.exe
#coding=utf-8

import cgi, cgitb, json
import pandas as pd
from module.PredictModel import PredictModel
from module.updateModel import ClassifierModel,updateData
import codecs, sys, os
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

print('Content-Type: text/html; charset=utf8')
print("")

parameter = cgi.FieldStorage()
sentence_json = parameter.getvalue('sentence_json')
segment_json = parameter.getvalue('segment_json')
print(sentence_json)
# path = parameter.getvalue('path')
# member_id = parameter.getvalue('member_id')
# project_id = parameter.getvalue('project_id')
sentence_dict = json.loads(sentence_json)
segment_dict = json.loads(segment_json)

print(updateData(sentence_dict,segment_dict))

