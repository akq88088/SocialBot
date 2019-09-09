#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright 2017 Hai Liang Wang <hailiang.hl.wang@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# File: wordseg-algorithm/mmseg_example.py
# Author: Hai Liang Wang
# Date: 2017-07-19:22:25:38
#
#===============================================================================

"""
	MMSEG: 
	A Word Identification System for Mandarin Chinese Text Based on Two
	Variants of the Maximum Matching Algorithm
	http://technology.chtsai.org/mmseg/

	Other references:
	http://blog.csdn.net/nciaebupt/article/details/8114460
	http://www.codes51.com/itwd/1802849.html

	Dict:
	https://github.com/Samurais/jieba/blob/master/jieba/dict.txt

	Deps:
	Python3
"""

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__	= "Hai Liang Wang"
__date__	  = "2017-07-19:22:25:38"


import os
import sys
curdir = os.getcwd()
sys.path.append(curdir)

import math
import string
from functools import reduce 

class Word():
	'''
	A single word
	'''
	def __init__(self, text="", freq=0):
		self.text = text
		self.freq = freq
		self.length = len(text)

class Chunk():
	'''
	Word Group that split with Forward Maximum Match(FMM)
	'''

	def __init__(self, w1, w2 = None, w3 = None):
		self.words = []
		self.words.append(w1)
		if w2: self.words.append(w2)
		if w3: self.words.append(w3)

	@property
	def total_word_length(self):
		return reduce(lambda x, y: x + y.length, self.words, 0)

	@property
	def average_word_length(self):
		return float(self.total_word_length) / float(len(self.words))

	@property
	def standard_deviation(self):
		return math.sqrt(reduce(lambda x,y: x + \
						(y.length - self.average_word_length)**2, \
						self.words, 0.0) / self.total_word_length)
	@property
	def word_frequency(self):
		return reduce(lambda x, y: x + y.freq, self.words, 0)


class Vocabulary():
	'''
	Vocabulary with whole words
	'''

	def __init__(self, dict_path):
		self.dict = {}
		self.dict_path = dict_path
		self.max_word_length = 0
		self.__load()

	def __load(self):
		with open(self.dict_path,encoding='utf8') as f:
			for x in f.readlines():
				text, freq, tag = x.split()
				self.dict[text] = (len(text), int(freq), tag)
				self.max_word_length = max([self.max_word_length, len(text)])

	def get_word(self, text):
		if text in self.dict: 
			return Word(text=text, freq=self.dict[text][1])


class Tokenizer():
	'''
	MMSEG Tokenizer for Python
	'''
	def __init__(self, dict_path):
		self.V = Vocabulary(dict_path=dict_path)

	def cut(self, sentence):
		#去掉非字典字
		temp = ''
		for chr in sentence:
			if chr in self.V.dict:
				temp+=chr

		sentence = temp
		sentence_length = len(sentence)
		cursor = 0

		while cursor < sentence_length:
			if self.is_chinese_char(sentence[cursor]):
				chunks = self.__get_chunks(sentence, cursor) # Matching Algorithm
				words, length = self.__ambiguity_resolution(chunks) # Ambiguity Resolution Rules
				cursor += length
				for term in list(filter(None, words)): yield term
			else: # 处理非中文单词(英文单词, etc.)
				word, cursor = self.__match_none_chinese_words(sentence, cursor)
				if word:
					yield word

	def __ambiguity_resolution(self, chunks):
		'''
		根据当前游标位置进行切词
		'''
		# print("# Rule 1: 根据 total_word_length 进行消岐")
		# for x in chunks: [print(y.text) for y in x.words]; print('-'*20)
		if len(chunks) > 1: # Rule 1: 根据 total_word_length 进行消岐
			score = max([x.total_word_length for x in chunks])
			chunks = list(filter(None, \
							[ x if x.total_word_length == score \
								else None for x in chunks]))

		# print("# Rule 2: 根据 average_word_length 进行消岐") 
		# for x in chunks: [print(y.text) for y in x.words]; print('-'*20)
		if len(chunks) > 1: # Rule 2: 根据 average_word_length 进行消岐
			score = max([x.average_word_length for x in chunks])
			chunks = list(filter(None, \
							[ x if x.average_word_length == score \
								else None for x in chunks]))

		if len(chunks) > 1: # Rule 3: 根据 standard_deviation 进行消岐
			# 這個要挑小的他寫挑大的 被我抓到 已改
			score = min([x.standard_deviation for x in chunks])
			chunks = list(filter(None, \
							[ x if x.standard_deviation == score \
								else None for x in chunks]))

		if len(chunks) > 1: # Rule 4: 根据 word_frequency 进行消岐
			score = max([x.word_frequency for x in chunks])
			chunks = list(filter(None, \
							[ x if x.word_frequency == score \
								else None for x in chunks]))

		if len(chunks) != 1: 
			'''
			分词失败
			'''
			# 隨便挑一個
			# print('失敗')
			# return ''

		words = chunks[0].words
		return [w.text for w in words], reduce(lambda x,y: x + y.length, words ,0)

	def __get_chunks(self, sentence, cursor):
		'''
		根据游标位置取词组
		'''
		chunks = []
		chunk_begin = self.__match_chinese_words(sentence, cursor)
		for b in chunk_begin: 
			chunk_middle = self.__match_chinese_words(sentence, cursor + b.length)
			if chunk_middle:
				for m in chunk_middle:
					chunk_end = self.__match_chinese_words(sentence, cursor + b.length + m.length)
					if chunk_end:
						for e in chunk_end: 
							chunks.append(Chunk(b, m, e))
					else:
						chunks.append(Chunk(b, m))
			else:
				chunks.append(Chunk(b))
		
		# 這個是我用來檢查他有沒有算錯的部分
		# for chunk in chunks:
			# for word in chunk.words:
				# print(word.text,end=' ')
			# print(chunk.total_word_length,chunk.average_word_length,chunk.standard_deviation,chunk.word_frequency)
		# print()

		return chunks

	@staticmethod
	def __match_none_chinese_words(sentence, begin_pos):
		'''
		切割出非中文词
		'''
		# Skip pre-word whitespaces and punctuations
		#跳过中英文标点和空格
		cursor = begin_pos
		while cursor < len(sentence):
			ch = sentence[cursor]
			if Tokenizer.is_ascii_char(ch) or Tokenizer.is_chinese_char(ch):
				break
			cursor += 1
		#得到英文单词的起始位置	
		start = cursor
		
		#找出英文单词的结束位置
		while cursor < len(sentence):
			ch = sentence[cursor]
			if not Tokenizer.is_ascii_char(ch):
				break
			cursor += 1
		end = cursor
		
		#Skip chinese word whitespaces and punctuations
		#跳过中英文标点和空格
		while cursor < len(sentence):
			ch = sentence[cursor]
			if Tokenizer.is_ascii_char(ch) or Tokenizer.is_chinese_char(ch):
				break
			cursor += 1
			
		#返回英文单词和游标地址
		return sentence[start:end], cursor

	def __match_chinese_words(self, sentence, begin_pos):
		'''
		根据游标位置取词
		'''
		sentence_length = len(sentence)
		words = []
		cursor = begin_pos
		index = 0

		while cursor < sentence_length:
			if index >= self.V.max_word_length: break
			if not self.is_chinese_char(sentence[cursor]): break

			cursor += 1
			index += 1
			text = sentence[begin_pos:cursor]
			word = self.V.get_word(text)
			if word: words.append(word)

		# 這邊是多餘的 被我抓到
		# if not words: 
			# word = Word()
			# word.length = 0
			# words.append(word)

		return words

	@staticmethod
	def is_ascii_char(charater):
		if charater in string.whitespace:
			return False
		if charater in string.punctuation:
			return False
		return charater in string.printable

	@staticmethod 
	def is_chinese_char(charater):
		'''
		判断该字符是否是中文字符（不包括中文标点）
		'''  
		return 0x4e00 <= ord(charater) < 0x9fa6

def test_chunk_n_word():
	w1 = Word("中文", 1)
	w2 = Word("分词技术", 1)
	c1= Chunk(w1, w2)
	assert c1.total_word_length==6, "total_word_length"
	assert c1.average_word_length==c1.average_word_length , "average_word_length"
	assert c1.standard_deviation==0.5773502691896257 , "standard_deviation"
	assert c1.word_frequency==2, "word_frequency"
	print("passed.")

def test_vocab():
	# v = Vocabulary(dict_path=os.path.join(curdir, 'dict/8000words.txt'))
	t = Tokenizer(dict_path=os.path.join(curdir, 'dict/gov_dict_F.txt'))
	# print(len(v.dict))
	# print(v.get_word("中文").text)
	# print(v.get_word("中文").freq)
	# print(v.get_word("中文").length)
	print(' '.join(t.cut("研究生命來源")))
	print(' '.join(t.cut("南京市長江大橋歡迎您")))
	print(' '.join(t.cut("請把手抬高一點兒")))
	print(' '.join(t.cut("長春市長春節致詞")))#教育部辭典沒有長春這個詞 所以斷錯
	print(' '.join(t.cut("長春市長春藥店")))
	print(' '.join(t.cut("我的和服務必在明天做好。")))
	print(' '.join(t.cut("我發現有很多人喜歡她")))
	print(' '.join(t.cut("我喜歡看電視劇大長今")))
	print(' '.join(t.cut("一次性交出去很多錢")))
	print(' '.join(t.cut("我不喜歡日本和服")))

def test_token():
	t = Tokenizer(dict_path=os.path.join(curdir, 'dict/8000words.txt'))
	# for x in t.cut("CNN报道美国即将开始新一轮的单边制裁朝鲜计划"): print(x)
	print(' '.join(t.cut("CNN报道Washington D.C.即将开始新一轮的单边制裁朝鲜计划")))
	print(' '.join(t.cut("研究生命来源")))
	print(' '.join(t.cut("南京市长江大桥欢迎您")))
	print(' '.join(t.cut("请把手抬高一点儿")))
	print(' '.join(t.cut("长春市长春节致词。")))
	print(' '.join(t.cut("长春市长春药店。")))
	print(' '.join(t.cut("我的和服务必在明天做好。")))
	print(' '.join(t.cut("我发现有很多人喜欢他。")))
	print(' '.join(t.cut("我喜欢看电视剧大长今。")))
	print(' '.join(t.cut("半夜给拎起来陪看欧洲杯糊着两眼半晌没搞明白谁和谁踢。")))
	print(' '.join(t.cut("李智伟高高兴兴以及王晓薇出去玩，后来智伟和晓薇又单独去玩了。")))
	print(' '.join(t.cut("一次性交出去很多钱。 ")))
	print(' '.join(t.cut("这是一个伸手不见五指的黑夜。我叫孙悟空，我爱北京，我爱Python和C++。")))
	print(' '.join(t.cut("我不喜欢日本和服。")))
	print(' '.join(t.cut("雷猴回归人间。")))
	print(' '.join(t.cut("工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作")))
	print(' '.join(t.cut("我需要廉租房")))
	print(' '.join(t.cut("永和服装饰品有限公司")))
	print(' '.join(t.cut("我爱北京天安门")))
	print(' '.join(t.cut("abc")))
	print(' '.join(t.cut("隐马尔可夫")))
	print(' '.join(t.cut("雷猴是个好网站")))
	print(' '.join(t.cut("“Microsoft”一词由“MICROcomputer（微型计算机）”和“SOFTware（软件）”两部分组成")))
	print(' '.join(t.cut("草泥马和欺实马是今年的流行词汇")))
	print(' '.join(t.cut("伊藤洋华堂总府店")))
	print(' '.join(t.cut("中国科学院计算技术研究所")))
	print(' '.join(t.cut("罗密欧与朱丽叶")))
	print(' '.join(t.cut("我购买了道具和服装")))
	print(' '.join(t.cut("PS: 我觉得开源有一个好处，就是能够敦促自己不断改进，避免敞帚自珍")))
	print(' '.join(t.cut("湖北省石首市")))
	print(' '.join(t.cut("总经理完成了这件事情")))
	print(' '.join(t.cut("电脑修好了")))
	print(' '.join(t.cut("做好了这件事情就一了百了了")))
	print(' '.join(t.cut("人们审美的观点是不同的")))
	print(' '.join(t.cut("我们买了一个美的空调")))
	print(' '.join(t.cut("线程初始化时我们要注意")))
	print(' '.join(t.cut("一个分子是由好多原子组织成的")))
	print(' '.join(t.cut("祝你马到功成")))
	print(' '.join(t.cut("他掉进了无底洞里")))
	print(' '.join(t.cut("中国的首都是北京")))
	print(' '.join(t.cut("孙君意")))
	print(' '.join(t.cut("外交部发言人马朝旭")))
	print(' '.join(t.cut("领导人会议和第四届东亚峰会")))
	print(' '.join(t.cut("在过去的这五年")))
	print(' '.join(t.cut("还需要很长的路要走")))
	print(' '.join(t.cut("60周年首都阅兵")))
	print(' '.join(t.cut("你好人们审美的观点是不同的")))
	print(' '.join(t.cut("买水果然后来世博园")))
	print(' '.join(t.cut("买水果然后去世博园")))
	print(' '.join(t.cut("但是后来我才知道你是对的")))
	print(' '.join(t.cut("存在即合理")))
	print(' '.join(t.cut("的的的的的在的的的的就以和和和")))
	print(' '.join(t.cut("I love你，不以为耻，反以为rong")))
	print(' '.join(t.cut(" ")))
	print(' '.join(t.cut("")))
	print(' '.join(t.cut("hello你好人们审美的观点是不同的")))
	print(' '.join(t.cut("很好但主要是基于网页形式")))
	print(' '.join(t.cut("hello你好人们审美的观点是不同的")))
	print(' '.join(t.cut("为什么我不能拥有想要的生活")))
	print(' '.join(t.cut("后来我才")))
	print(' '.join(t.cut("此次来中国是为了")))
	print(' '.join(t.cut("使用了它就可以解决一些问题")))
	print(' '.join(t.cut(",使用了它就可以解决一些问题")))
	print(' '.join(t.cut("其实使用了它就可以解决一些问题")))
	print(' '.join(t.cut("好人使用了它就可以解决一些问题")))
	print(' '.join(t.cut("是因为和国家")))
	print(' '.join(t.cut("老年搜索还支持")))

if __name__ == '__main__':
	test_vocab()
	# test_token()