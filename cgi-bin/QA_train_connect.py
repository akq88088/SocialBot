import cgi, cgitb
import os
import pandas as pd
import numpy as np
import json
from module.QA_train import QA_train

# parameter = cgi.FieldStorage()
# text = parameter.getvalue('text')

QA_train = QA_train()
# data_dir = 'D:\\dektop\\work_data_backup_0923_2256\\rule_all.csv'
data_dir = 'D:\\dektop\\work_data_backup_0923_2256\\rule_all.csv'
QA_train.train(data_dir)
print("Content-type:text/html") #必須
print('') #必須
print('finish')