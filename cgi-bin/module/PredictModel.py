#coding=utf-8
import json,re
import numpy as np
from keras.models import load_model
from module.trainVecModel import Dictionary
from module.mmsegTest import Tokenizer
mmseg = Tokenizer('module/data/userDict.txt')

class PredictModel():
	def __init__(self,folder):
		self.folder = folder
		self.dic = Dictionary(folder)
		self.intToSen = {}
		self.loadModel()
		
	def loadModel(self):
		# print('載入分類模型')
		self.model = load_model(self.folder+'/sentimentPredict.h5')
		with open(self.folder+'/sentimentWord.json', encoding='utf8') as file:
			fileTexts = ''.join(file.readlines())
		self.sentimentWord = json.loads(fileTexts)
		with open(self.folder+'/intToSen.json', encoding='utf8') as file:
			fileTexts = ''.join(file.readlines())
		intToSen = json.loads(fileTexts)
		for key in intToSen:
			self.intToSen[int(key)]=intToSen[key]
		
	def makeVector(self,content):
		testSen = re.split('!|\?|。|，|！|？|；',content)
		if not testSen[-1]:
			testSen = testSen[:-1]
		testX,testSenSeg = [],[]
		for sentence in testSen:
			vector,size = np.zeros(100),0
			temp = []
			for seg in mmseg.cut(sentence):
				if seg in self.dic.dictionary:
					if seg in self.sentimentWord:
						temp.append(seg)
						vector += self.dic.dictionary[seg].vector
						size+=1
			if size!=0:
				vector /= size
			testX.append(vector)
			testSenSeg.append(temp)
		testX = np.array(testX)
		return testX,testSen,testSenSeg
		
	def predict(self,content):
		testX,testSen,testSenSeg = self.makeVector(content)
		predictions = self.model.predict_classes(testX)
		senRatio = {}
		for key in self.intToSen:
			senRatio[self.intToSen[key]] = 0
		for pre in predictions:
			senRatio[self.intToSen[pre]] += 1
		for key in senRatio:
			senRatio[key] /= len(predictions)
			senRatio[key] *= 100
		return senRatio
		
	def predictDetail(self,content):
		testX,testSen,testSenSeg = self.makeVector(content)
		predictions = self.model.predict_classes(testX)
		for idx,rate in enumerate(self.model.predict(testX)):
			print(testSen[idx],testSenSeg[idx])
			print('預測情緒:',self.intToSen[predictions[idx]])
			for i,r in enumerate(rate):
				print('%s: %.4f%%'%(self.intToSen[i],r*100))
		
if __name__ == '__main__':
	pdm = PredictModel('data')
	print(pdm.predict('真是太開心了!'))