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
QA_train.read_data_generate_rule_main()
print("Content-type:text/html") #必須
print('') #必須
print('QA rule generate finish')