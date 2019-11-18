#!D:/Python/Python36/python.exe
#!C:/ProgramData/Anaconda3/python.exe
#!D:/Anaconda3/python.exe
#coding=utf-8

import cgi, cgitb
from module.NER import NER
from module.NER import data_trans
import codecs, sys 
import os, re
import json
sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)

print('Content-Type: text/html; charset=utf8')
print("")

parameter = cgi.FieldStorage()
words = json.loads(parameter.getvalue('words'))
pos = json.loads(parameter.getvalue('pos'))
tags = json.loads(parameter.getvalue('tags'))
pid = parameter.getvalue('pid')
model_path = './module/model/'+ str(pid) +'/ner_model.h5'


words_ls, pos_ls, tags_ls = [],[],[]
start = 0
for i,w in enumerate(words):
	if re.match(r'[!?。！？」"，]', w):
		words_ls.append(words[start: i+1])
		pos_ls.append(pos[start: i+1])
		tags_ls.append(tags[start: i+1])
		start = i+1

dt =  data_trans()

NER = NER(model_path)
pos = dt.to_int(pos_ls, NER.pos_dict)
pos_pad = dt.padding(pos, maxlen=NER.maxlen, padding='pre')
tags = dt.to_int(tags_ls, NER.ner_dict)
tags_pad = dt.padding(tags, maxlen=NER.maxlen, padding='pre')
tags_onehot = dt.to_onehot(tags_pad, NER.ner_dict)
x = NER.train(pos_pad, tags_onehot, batch_size=1, epochs=10)
NER.save_model(model_path)
print(x)