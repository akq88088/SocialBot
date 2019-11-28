#coding=utf-8
import numpy as np
import json,re,random,heapq,os
import gensim
from keras.layers import Dense
from keras.models import Sequential
from keras.models import load_model
from keras.utils import to_categorical
from module.mmsegTest import Tokenizer
mmseg = Tokenizer('module/data_kenlee/userDict.txt')

def isChinese(cks):
	import re
	chinese = re.compile(u'[\u4e00-\u9fa5]+')
	number = re.compile(u'[\u0030-\u0039]')
	english = re.compile(u'[\u0041-\u005a\u0061-\u007a]')
	if chinese.search(cks) and not number.search(cks) and not english.search(cks):
		return True
	else:
		return False

def cosine_distance(matrix1,matrix2):
	import numpy as np
	matrix1_matrix2 = np.dot(matrix1, matrix2.transpose())
	matrix1_norm = np.sqrt(np.multiply(matrix1, matrix1).sum(axis=1))
	matrix1_norm = matrix1_norm[:, np.newaxis]
	matrix2_norm = np.sqrt(np.multiply(matrix2, matrix2).sum(axis=1))
	matrix2_norm = matrix2_norm[:, np.newaxis]
	cosine_distance = np.divide(matrix1_matrix2, np.dot(matrix1_norm, matrix2_norm.transpose()))
	return cosine_distance.tolist()

class Word():
	def __init__(self,text='',definition=''):
		self.text = text
		self.definition = definition
		self.defSeg = []
		self.vector = []

class Dictionary():
	def __init__(self,folder):
		self.dictionary = {}
		self.wordToInt = {}
		self.intToWord = {}
		self.folder = folder
		self.pickWordPath = folder+'/pickWord.txt'
		self.stopWordPath = folder+'/stopWord.txt'
		self.dictPath = folder+'/govDict.json'
		self.loadDictionary()
		self.amount = len(self.dictionary)
	def loadDictionary(self):
		if os.path.isfile(self.folder+'/definition_seg.txt'):
			# print('有斷好的詞典可以load')
			self.readResult()
			return
		allWords,stopWords,pickWords = [],[],[]
		with open(self.dictPath, encoding='utf8') as file:
			fileTexts = ''.join(file.readlines())
		twdict = json.loads(fileTexts)
		rule = '（.*）|\(.*\)|（.*\)|\(.*）'
		#讀比較常用 挑選過 需要的詞 
		with open(self.pickWordPath, 'r', encoding='utf8') as file:
			for pw in file.readlines():
				pickWords.append(pw.strip())
		#讀取停用詞
		with open(self.stopWordPath, encoding='utf8') as file:
			for sw in file.readlines():
				stopWords.append(sw.strip())
		#建立Word類別
		global mmseg
		for word in twdict:
			title = word['title'].strip()
			title = re.sub(rule,'',title)
			definition, definition_temp = '', ''
			if not isChinese(title) or title not in pickWords:
				continue
			#取詞的定義
			for heteronym in word['heteronyms']:
				for mean in heteronym['definitions']:
					definition_temp += mean['def']
					if 'synonyms' in mean:
						definition_temp += (mean['synonyms']+'。')
			for d in definition_temp.split('。'):
				if '：' not in d:
					definition += (d+'，')
			if definition:
				self.dictionary[title] = Word(title,definition+title)
		#定義斷詞
		for key in self.dictionary:
			for seg in set(mmseg.cut(self.dictionary[key].definition)):
				if seg not in stopWords and seg in pickWords:
						self.dictionary[key].defSeg.append(seg)
		for key in self.dictionary:
			if len(self.dictionary[key].defSeg)==2:
				w = self.dictionary[key].defSeg[0]
				for seg in self.dictionary[w].defSeg:
					self.dictionary[key].defSeg.append(seg)
		#產生編號
		words = self.dictionary.keys()
		self.wordToInt = {w:c for c,w in enumerate(words)}
		self.intToWord = {c:w for c,w in enumerate(words)}
		
	def readResult(self):
		with open(self.folder+'/definition.txt', encoding='utf8') as file:
			for line in file.readlines():
				line = line.strip()
				result = line.split(' ')
				title,definition = result[0].strip(),result[1].strip()
				self.dictionary[title] = Word(title,definition)
		with open(self.folder+'/definition_seg.txt', encoding='utf8') as file:
			for line in file.readlines():
				line = line.strip()
				result = line.split(' ')
				title,defSeg = result[0].strip(),result[1:]
				self.dictionary[title].defSeg = defSeg
		with open(self.folder+'/intToWord.txt', encoding='utf8') as file:
			temp = dict()
			for line in file.readlines():
				result = line.split(' ')
				key,value = int(result[0]),result[1].strip()
				temp[key] = value
			self.intToWord = temp
		with open(self.folder+'/wordToInt.txt', encoding='utf8') as file:
			temp = dict()
			for line in file.readlines():
				result = line.split(' ')
				key,value = result[0].strip(),int(result[1])
				temp[key] = value
			self.wordToInt = temp
		with open(self.folder+'/wordVector.json', encoding='utf8') as file:
			fileTexts = ''.join(file.readlines())
		wv = json.loads(fileTexts)
		for word in wv:
			if word in self.dictionary:
				self.dictionary[word].vector = np.array(wv[word])
		
class VectorModel():
	def __init__(self,folder):
		self.folder = folder
		self.dic = Dictionary(folder=folder)
		if os.path.isfile(self.folder+'/def2vec.h5'):
		# 	# print('有model可以load')
			self.model = load_model(folder+'/def2vec.h5')
		if os.path.isfile(self.folder+'/govDict_w2v.model'):
			self.w2v_model = gensim.models.Word2Vec.load(self.folder+'/govDict_w2v.model')
		
	def trainWordVec(self,vectorLen=100):
		self.model = Sequential()
		self.model.add(Dense(vectorLen, input_dim=self.dic.amount, activation='linear'))
		self.model.add(Dense(self.dic.amount, activation='softmax'))
		self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
		self.model.fit_generator(self.trainDataGenerator(), steps_per_epoch=(self.dic.amount//6)+1, epochs=25, verbose=2)
		# for i,vec in enumerate(self.model.get_weights()[0]):
			# self.dic.dictionary[self.intToWord[i]].vector = vec
		
	def getSimilar(self,text):
	# 	distanceResult = cosine_distance([self.model.get_weights()[0][self.dic.wordToInt[text]]],self.model.get_weights()[0])
	# 	topIndex = map(distanceResult[0].index, heapq.nlargest(20, distanceResult[0]))
	# 	for i in topIndex:
	# 		if distanceResult[0][i]>0.5:
	# #			print(distanceResult[0][i],self.intToWord[i])
	# 			yield self.dic.intToWord[i]
		for sim in w2v_model.wv.most_similar(word,topn=1000):
			if sim[1]>0.6:
				yield self.dic.intToWord[i]
		
	def saveAll(self):
		with open(self.folder+'/definition.txt', 'w', encoding='utf8') as file:
			for title in self.dic.dictionary:
				file.write(title+' '+self.dic.dictionary[title].definition.strip())
				file.write('\n')
		with open(self.folder+'/definition_seg.txt', 'w', encoding='utf8') as file:
			for title in self.dic.dictionary:
				file.write(title+' '+' '.join(self.dic.dictionary[title].defSeg))
				file.write('\n')
		with open(self.folder+'/intToWord.txt', 'w', encoding='utf8') as file:
			for key in self.dic.intToWord:
				file.write(str(key)+' '+self.dic.intToWord[key])
				file.write('\n')
		with open(self.folder+'/wordToInt.txt', 'w', encoding='utf8') as file:
			for key in self.dic.wordToInt:
				file.write(key+' '+str(self.dic.wordToInt[key]))
				file.write('\n')
		dicVec = {}
		for word in self.dic.dictionary:
			dicVec[word] = self.model.get_weights()[0][self.dic.wordToInt[word]].tolist()
		with open(self.folder+'/wordVector.json', 'w', encoding='utf8') as fp:
			json.dump(dicVec, fp, ensure_ascii=False)
		self.model.save(self.folder+'/def2vec.h5')
		
	def trainDataGenerator(self):
		while(True):
			X,Y,i = [],[],0
			randomVocab = random.sample(self.dic.dictionary.keys(),self.dic.amount)
			for c,voc in enumerate(randomVocab):
				# print('%.2f%%'%(c*100/self.dic.amount),end='\r')
				if len(self.dic.dictionary[voc].defSeg)>0:
					i += 1
					xtemp = to_categorical(self.dic.wordToInt[voc],num_classes=self.dic.amount)
					for seg in self.dic.dictionary[voc].defSeg:
						ytemp = to_categorical(self.dic.wordToInt[seg],num_classes=self.dic.amount)
						X.append(xtemp)
						Y.append(ytemp)
						if i == 6:
							yield np.array(X),np.array(Y)
							X,Y,i = [],[],0
	
if __name__ == '__main__':
	VM = VectorModel('data')
	VM.trainWordVec()
	VM.saveAll()