# coding: utf-8

import re
import jieba
from bosonnlp import BosonNLP

class TextProcessor():
    def __init__(self):
        pass
    
    def _read_stopwords(self, path='../stop_words.txt'):
        stop_words = set()
        with open(path, 'r', encoding='utf8') as f:
            [stop_words.add(line.strip()) for line in f.readlines()]
            
        return stop_words
        
    def sentence_break(self, text, split_char='!?。！？'):
        sentences = []
        start = 0
        for i, char in enumerate(text):
            if char in split_char:
                if start == i:
                    sentences[-1] += text[i]
                else:
                    sentences.append(text[start:i+1])
                start = i + 1
                
        if start < len(text):
            sentences.append(text[start:len(text)])
            
        return sentences
    
    def _boson_seg(self, text):
        nlp = BosonNLP('g8lQg9Mv.25818.fAbbwt6TYhh8')
        if type(text) == str:
            text = [text]
        
        corpus_len = len(text)
        word, tag = [], []
        for idx in range(corpus_len//100 + 1):
            curr_idx = idx*100
            result = nlp.tag(text[curr_idx: min(curr_idx+100, corpus_len)])
            for seg in result:
                word.append(seg['word'])
                tag.append(seg['tag'])
        
        return word
    
    def _jieba_seg(self, text):
        if type(text) == str:
            segments = [jieba.cut(text)]
        else:
            segments = []
            for s in text:
                seg = jieba.cut(s)
                segments.append(seg)
                
        return segments
    
    def segement(self, text, seg_fn='boson', use_stopwords=True):
        try:
            seg_fn = {'boson': self._boson_seg, 'jieba': self._jieba_seg}[seg_fn]
        except:
            raise 'seg_fn only boson or jieba'
            return
        
        segments = seg_fn(text)

        if use_stopwords:
            stop_words = self._read_stopwords()
        else: stop_words = set()

        segments_new = []
        for seg in segments:
            seg = [s for s in seg if s not in stop_words]
            seg = ' '.join(seg)
            segments_new.append(seg)

        return segments_new

