# coding: utf-8
import re
import os
import jieba
import jieba.posseg
from bosonnlp import BosonNLP
import random
cwd = os.path.dirname(__file__)

class TextProcessor():
    def __init__(self):
        self.boson_key_list = ['g8lQg9Mv.25818.fAbbwt6TYhh8',
        'Xrzs7xvr.26748.xUoREj5Sgifi',
        'ySsYfLMS.26746.MrODj8fAYeQu',
        'DOeszme9.26747.xg3lcXi7Jun4',
        '8EP496lI.26743.mNK0Tk6Rpk5F',
        'qiVsBy45.26744.9-U4aaXH2yEs']
    
    def _read_stopwords(self, path=cwd+'/data_alex/stop_words.txt'):
        stop_words = set()
        with open(path, 'r', encoding='utf8') as f:
            [stop_words.add(line.strip()) for line in f.readlines()]
            
        return stop_words
        
    def sentence_break(self, text, split_char='!?。！？」"'):
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
        boson_key = self.boson_key_list[random.randint(0,len(self.boson_key_list)- 1)]
        nlp = BosonNLP(boson_key)
        if type(text) == str:
            text = [text]
        
        corpus_len = len(text)
        words, tags = [], []
        for idx in range(corpus_len//100 + 1):
            curr_idx = idx*100
            result = nlp.tag(text[curr_idx: min(curr_idx+100, corpus_len)])
            for seg in result:
                words.append(seg['word'])
                tags.append(seg['tag'])
        
        return words, tags
    
    def _jieba_seg(self, text):
        if type(text) == str:
            text = [text]
        
        words, tags = [], []
        for s in text:
            posseg = [seg for seg in jieba.posseg.cut(s.strip())]
            w, t = list(zip(*posseg))
            w, t = list(w), list(t)
            words.append(w)
            tags.append(t)
                
        return words, tags
    
    def segment(self, text, seg_fn='boson', use_stopwords=True):
        try:
            seg_fn = {'boson': self._boson_seg, 'jieba': self._jieba_seg}[seg_fn]
        except:
            raise 'seg_fn only boson or jieba'
            return
        
        segments = seg_fn(text)[0]

        if use_stopwords:
            stop_words = self._read_stopwords()
        else: stop_words = set()

        segments_new = []
        for seg in segments:
            seg = [s for s in seg if s not in stop_words]
            seg = ' '.join(seg)
            segments_new.append(seg)

        return segments_new

    def seg_tag(self, text, seg_fn='boson', use_stopwords=True):
        try:
            pos_set = {'boson':['n', 'nr1', 'nrf', 'nr', 'ns','t','s','f','v', 'vshi', 'vyou', 'vn', 'a','b','z','r','m','q','d','p','c','u','o','y','h','k','nx','w'], 
                        'jieba':['n', 'ng', 'nr', 'ns', 'nt', 'nz', 'v', 'vd', 'vg', 'vi', 'vn', 'a', 'ad', 'ag', 'an', 'b','c','d','e','f','g','h','i','j','k','l', 'm', 'mq', 'o','p','q', 'r', 'rg', 'rr', 'rz', 's', 't', 'tg', 'u', 'ud', 'ug', 'uj', 'ul', 'uv', 'uz', 'w', 'x','y','z']}[seg_fn]
            seg_fn = {'boson': self._boson_seg, 'jieba': self._jieba_seg}[seg_fn]
        except Exception as e:
            print(e)
            raise 'seg_fn only boson or jieba'
            return

        words, tags = seg_fn(text)

        if use_stopwords:
            stop_words = self._read_stopwords()
        else: stop_words = set()

        words_new, tags_new= [], [] 
        for w, t in zip(words,tags):
            temp_w, temp_t = [],[]
            for w_in, t_in in zip(w,t):
                if w_in not in stop_words:
                    temp_w.append(w_in)
                    if t_in not in pos_set:
                        t_in = t_in[0]
                    temp_t.append(t_in)
            words_new.append(temp_w)
            tags_new.append(temp_t)

        return words_new, tags_new

if __name__ == '__main__':
    tp = TextProcessor()
    # text = '小明喜歡小美'
    print(tp.sentence_break('他看到老師說：「老師好！」'))
    # print(tp.seg_tag(text, seg_fn='jieba', use_stopwords=False))
    # print(tp.seg_tag(text, use_stopwords=False))