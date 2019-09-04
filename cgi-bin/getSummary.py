#!C:/Users/mcu/AppData/Local/Programs/Python/Python36/python.exe
#!D:/Python/Python36/python.exe
#!D:/Python3.4.3/python.exe
#coding=utf-8

import cgi, cgitb
from module import TextSummary
from module import TextProcessor
import codecs, sys 
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

print('Content-Type: text/html; charset=utf8')
print("")

parameter = cgi.FieldStorage()
algorithm = parameter.getvalue('algorithm')
percentage = float(parameter.getvalue('percentage'))
text = parameter.getvalue('text')

process = TextProcessor.TextProcessor()

algoritm_dic = {"textsim": TextSummary.TextSim_TextSum(process),
				"textrank": TextSummary.TextRank_TextSum(process),
				"textmap": TextSummary.TRMap_TextSum(process)}

Summary = algoritm_dic[algorithm]
print(" ".join(Summary.summary(text, compression_ratio=percentage)))