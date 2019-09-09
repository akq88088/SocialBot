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

class DataSet():
	def __init__(self,folder):
		self.folder = folder
		self.dataPath = folder+'/SentenceLabel.csv'
		# self.stmPath = folder+'/sentimentWord.txt'
		self.title = []
		self.sentence = []
		self.sentiment = []
		self.sentimentSum = []
		self.sentimentWord = {}
		self.loadData()
		self.generStmWord()
	def loadData(self):
		data = pd.read_csv(self.dataPath,header=None)
		self.title = data.values[0][1:] 
		self.sentence = data.values[1:,0]
		self.sentiment = data.values[1:,1:].astype(int)
		self.sentimentSum = np.sum(self.sentiment, axis = 0)
	def generStmWord(self):
		global mmseg
		VM = VectorModel(self.folder)
		wordSD,wordCount = {},{}
		for i,st in enumerate(self.sentence):
			for seg in mmseg.cut(st):
				#--
				if seg in wordCount:
					wordCount[seg]+=1
				else:
					wordCount[seg]=1
				#--
				if seg not in wordSD:
					wordSD[seg] = np.zeros(len(self.sentimentSum))
				for j,stm in enumerate(self.sentiment[i]):
					if stm==1:
						wordSD[seg][j]+=1
#					 else:
#						 wordSD[seg][j]-=1
		for word in wordSD:
			if word in VM.dic.dictionary:
				wordSD[word]/=wordCount[word]
#				 print(wordSD)
				for i,sd in enumerate(wordSD[word][:-1]):
					if sd>0.7:
						self.sentimentWord[word] = self.title[i]
						# print(word,self.title[i])
						for sw in VM.getSimilar(word):
							# print(sw)
							self.sentimentWord[sw] = self.title[i]
						# print('-------------')
#		 for word in wordSD:
#			 if word in dic.dictionary:
#				 wordSD[word]/=(self.sentimentSum+1)
#				 for sd in wordSD[word][:-1]:
#					 if sd>0.0:
#						 self.sentimentWord.add(word)
#						 for sw in dic.getSimilar(word):
#							 self.sentimentWord.add(sw)
		self.sentimentWord['不'] = '反'
		self.sentimentWord['不要'] = '反'
		self.sentimentWord['不會'] = '反'
		self.sentimentWord['不用'] = '反'
		self.sentimentWord['不再'] = '反'
		self.sentimentWord['沒有'] = '反'
		
	def getTrainData(self,dic,seg=False):
		X,Y = [],[]
		for i,st in enumerate(self.sentence):
#			 print(st)
			stv,size=np.zeros(100),1
			for seg in mmseg.cut(st):
				if seg in self.sentimentWord:
#					 print(seg,end=' ')
					size+=1
					stv+=dic.dictionary[seg].vector
#			 print(stv/size)
#			 print('--------------')
			X.append(stv/size)
			Y.append(self.sentiment[i])
		return np.array(X),np.array(Y)
			
	def getTestData(self,dic):
		X,Y = [],[]
		sentenceSeg = []
		for i,st in enumerate(self.sentence):
#			 print(st)
			stv,size,temp=np.zeros(100),1,[]
			for seg in mmseg.cut(st):
				if seg in self.sentimentWord:
					size+=1
					stv+=dic.dictionary[seg].vector
					temp.append(seg)
			X.append(stv/size)
			Y.append(self.sentiment[i])
			sentenceSeg.append(temp)
		return np.array(X),np.array(Y),sentenceSeg
		
class ClassifierModel():
	def __init__(self,folder):
		self.folder = folder
		self.DT = Dictionary(folder)
		self.DS = DataSet(folder)
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
		with open(self.folder+'/intToSen.json', 'w', encoding='utf8') as fp:
			json.dump(intToSen, fp, ensure_ascii=False)
		with open(self.folder+'/sentimentWord.json', 'w', encoding='utf8') as fp:
			json.dump(self.DS.sentimentWord, fp, ensure_ascii=False)
		self.model.save(self.folder+'/sentimentPredict.h5')
	
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