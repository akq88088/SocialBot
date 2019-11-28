#coding=utf-8
import pandas as pd
import numpy as np
import json
from keras.layers import Dense
from keras.models import Sequential
from keras.models import load_model
from keras.utils import to_categorical
from module.trainVecModel import VectorModel,Dictionary
from module.mmsegTest import Tokenizer
mmseg = Tokenizer('module/data_kenlee/userDict.txt')

def updateData(sentence_dict,segment_dict,path=""):
	originData = pd.read_csv('module/data_kenlee/SentenceLabel.csv',header=None)
	senToInt = {'喜歡':0,'憤怒':1,'難過':2,'驚訝':3,'害怕':4,'無表情':5}
	title = originData.values[0][1:]
	sentence = list(originData.values[1:,0])
	sentiment = list(originData.values[1:,1:].astype(int))
	print(sentence_dict)
	for sen in sentence_dict:
		sentence.append(sen)
		temp = [0,0,0,0,0,0]
		print(sen)
		print(sentence_dict[sen])
		temp[senToInt[sentence_dict[sen]]] = 1
		sentiment.append(temp)
	with open('module/data_kenlee/member_id/project_id/SentenceLabel.csv', 'w', encoding='utf8') as file:
		file.write('\ufeff')
		file.write('句子,喜歡,憤怒,難過,驚訝,害怕,無表情\n')
		for i,sen in enumerate(sentence):
			file.write(sen)
			file.write(',')
			file.write(','.join(str(x) for x in sentiment[i]))
			file.write('\n')
	with open('module/data_kenlee/member_id/project_id/sentimentWord.json', encoding='utf8') as file:
		fileTexts = ''.join(file.readlines())
		originSentimentWord = json.loads(fileTexts)
	for seg in segment_dict:
		if segment_dict[seg]!='無表情':
			originSentimentWord[seg] = segment_dict[seg]
		else:
			if seg in originSentimentWord:
				originSentimentWord.pop(seg)
	with open('module/data_kenlee/member_id/project_id/sentimentWord.json', 'w', encoding='utf8') as fp:
		json.dump(originSentimentWord, fp, ensure_ascii=False)
	model = ClassifierModel('module/data_kenlee')
	model.saveAll()
	print('完成')


class DataSet():
	def __init__(self,folder,member_id="member_id",project_id="project_id",data_name="SentenceLabel.csv"):
		self.folder = folder
		self.dataPath = folder+'/'+member_id+'/'+project_id+'/'+data_name
		# self.stmPath = folder+'/sentimentWord.txt'
		self.title = []
		self.sentence = []
		self.sentiment = []
		self.sentimentWord = {}
		self.loadData()
	def loadData(self):
		data = pd.read_csv(self.dataPath,header=None)
		self.title = data.values[0][1:] 
		self.sentence = data.values[1:,0]
		self.sentiment = data.values[1:,1:].astype(int)
		with open('module/data_kenlee/member_id/project_id/sentimentWord.json', encoding='utf8') as file:
			fileTexts = ''.join(file.readlines())
			self.sentimentWord = json.loads(fileTexts)
		
	def getTrainData(self,dic,seg=False):
		X,Y = [],[]
		for i,st in enumerate(self.sentence):
#			 print(st)
			stv,size=np.zeros(100),1
			for seg in mmseg.cut(st):
				if seg in self.sentimentWord:
					if seg in dic.dictionary:
	#					 print(seg,end=' ')
						size+=1
						stv+=dic.dictionary[seg].vector
#			 print(stv/size)
#			 print('--------------')
			X.append(stv/size)
			Y.append(self.sentiment[i])
		return np.array(X),np.array(Y)
		
class ClassifierModel():
	def __init__(self,folder,member_id="member_id",project_id="project_id",data_name="SentenceLabel.csv"):
		self.folder = folder
		self.projectPath = folder+'/'+member_id+'/'+project_id
		self.DT = Dictionary(folder)
		self.DS = DataSet(folder,member_id,project_id,data_name)
		self.model = Sequential()
		self.trainClsModel()
	
	def trainClsModel(self):
		X,Y = self.DS.getTrainData(self.DT)
		self.model.add(Dense(50, input_dim=len(X[0]), activation='relu'))
		self.model.add(Dense(100, activation='relu'))
		self.model.add(Dense(50, activation='relu'))
		self.model.add(Dense(len(Y[0]), activation='softmax'))
		self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
		self.model.fit(X,Y, epochs=100, batch_size=100, verbose=2)
	
	def saveAll(self):
		intToSen = {}
		for i,sen in enumerate(self.DS.title):
			intToSen[int(i)] = sen
		with open(self.projectPath+'/intToSen.json', 'w', encoding='utf8') as fp:
			json.dump(intToSen, fp, ensure_ascii=False)
		with open(self.projectPath+'/sentimentWord.json', 'w', encoding='utf8') as fp:
			json.dump(self.DS.sentimentWord, fp, ensure_ascii=False)
		self.model.save(self.projectPath+'/sentimentPredict.h5')
	
	def evaluation(self):
		intToSen = {0:'喜',1:'怒',2:'哀',3:'驚',4:'怕',5:'無'}
		X,Y,sentenceSeg = self.DS.getTestData(self.DT)
		prediction = self.model.predict(X,verbose=1)        
		print(pd.crosstab(np.argmax(Y,axis=1),np.argmax(prediction,axis=1),rownames=['label'],colnames=['predict']))
		predictions = self.model.predict_classes(X)
		for idx,rate in enumerate(self.model.predict(X)):
			if Y[idx][predictions[idx]]!=1:
				print(self.DS.sentence[idx],sentenceSeg[idx])
				print('預測情緒:',intToSen[predictions[idx]])
				for i,r in enumerate(rate):
					print('%s: %.4f%%'%(intToSen[i],r*100))

if __name__ == '__main__':
	CM = ClassifierModel('data')