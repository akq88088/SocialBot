#!C:/Users/mcu/AppData/Local/Programs/Python/Python36/python.exe
#!D:/Python/Python36/python.exe
#!D:/Anaconda3/python.exe
#coding=utf-8

import cgi, cgitb
from module import TextSummary
import codecs, sys 
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

print('Content-Type: text/html; charset=utf8')
print("")

parameter = cgi.FieldStorage()
algorithm = parameter.getvalue('algorithm')
percentage = float(parameter.getvalue('percentage'))
text = parameter.getvalue('text')

algoritm_dic = {"textsim": TextSummary.TextSim_TextSum(),
				"textrank": TextSummary.TextRank_TextSum(),
				"textmap": TextSummary.TRMap_TextSum()}

Summary = algoritm_dic[algorithm]
print(" ".join(Summary.summary(text, compression_ratio=percentage)))
