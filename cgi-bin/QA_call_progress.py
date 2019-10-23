#!D:/Python/Python36/python.exe
#!C:/ProgramData/Anaconda3/python.exe
import cgi, cgitb
import os
import pandas as pd
import numpy as np
import json
from module.QA_train import QA_train

parameter = cgi.FieldStorage()
owner = parameter.getvalue('owner')
p_name = parameter.getvalue('p_name')
QA_train = QA_train(owner,p_name)

try:
    progress_rate = QA_train.read_rule_progress()
except:
    progress_rate = "0"
print("Content-type:text/html") #必須
print('') #必須
print(progress_rate)