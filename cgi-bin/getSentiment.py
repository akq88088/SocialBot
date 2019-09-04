#!C:/Users/mcu/AppData/Local/Programs/Python/Python36/python.exe
#!D:/Python/Python36/python.exe
#!D:/Python3.4.3/python.exe
#coding=utf-8

import cgi, cgitb
from module_k.PredictModel import PredictModel
import codecs, sys, os
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

print('Content-Type: text/html; charset=utf8')
print("")

parameter = cgi.FieldStorage()
text = parameter.getvalue('text')
cwd = os.getcwd()
pdm = PredictModel(cwd+"/module_k/data")
print(pdm.predict(text))