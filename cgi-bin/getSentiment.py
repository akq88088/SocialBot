#!D:/Python/Python36/python.exe
#!D:/Anaconda3/python.exe
#!C:/Users/mcu/AppData/Local/Programs/Python/Python36/python.exe
#coding=utf-8

import cgi, cgitb
from module.PredictModel import PredictModel
import codecs, sys, os
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

print('Content-Type: text/html; charset=utf8')
print("")

parameter = cgi.FieldStorage()
text = parameter.getvalue('text')
cwd = os.getcwd()
pdm = PredictModel(cwd+"/module/data_kenlee")
print(pdm.predict(text))