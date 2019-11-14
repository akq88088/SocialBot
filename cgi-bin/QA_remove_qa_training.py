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
# owner = "c2525a7f58ae3776070e44c106c48e15"
# p_name = "tt"
QA_train = QA_train(owner,p_name)
QA_train.remove_qa_training()
print("Content-type:text/html") #必須
print('') #必須
print('QA remove qa training finish')