# coding: utf-8
from keras.models import Sequential
from keras.layers import Dense, LSTM, InputLayer, Bidirectional, TimeDistributed, Embedding, Activation
from keras.optimizers import Adam
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import csv
import os
import numpy as np
import json
try:
    import TextProcessor
except:
    from module import TextProcessor

cwd = os.path.dirname(__file__)

class NER():
    def __init__(self, model_path, maxlen=30,
                    posDict_path = cwd+'/model/ner_init/pos_dict.txt',
                    nerDict_path = cwd+'/model/ner_init/ner_dict.txt'):
        try:
            self.model = load_model(model_path)
        except:
            self.model = load_model(cwd+'/model/ner_init/ner_model.h5')
        
        with open(posDict_path) as f: self.pos_dict = json.load(f)
        with open(nerDict_path) as f: self.ner_dict = json.load(f)

        self.TextProcessor = TextProcessor.TextProcessor()
        self.transformer = data_trans()
        self.maxlen = maxlen

    def build_model(self, input_len, input_dim, output_dim, embed_units, lstm_units):
        model = Sequential()
        model.add(InputLayer(input_shape=(input_len, )))
        model.add(Embedding(input_dim, embed_units))
        model.add(Bidirectional(LSTM(lstm_units, return_sequences=True)))
        model.add(TimeDistributed(Dense(output_dim)))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy',
                    optimizer=Adam(0.01),
                    metrics=['accuracy'])
        self.model = model

    def train(self, X, Y, batch_size=1, epochs=1, validation_split=0.1):
        self.model.fit(X, Y, batch_size=batch_size, epochs=epochs)

    def save_model(self, path):
        self.model.save(path)

    def predict(self, data):
        sentence = self.TextProcessor.sentence_break(data, split_char='!?。！？,，」"')

        segment = []
        part_of_speach = []
        result = []
        for sent in sentence:
            words, tags = self.TextProcessor.seg_tag(sent, use_stopwords=False)
            words = words[0]

            sent_len = len(words)

            pos = self.transformer.to_int(tags, self.pos_dict)

            pos_pad = self.transformer.padding(pos, maxlen=self.maxlen, padding='pre')
            
            try:
                ner = [np.argmax(i) for i in self.model.predict(pos_pad.reshape(1,self.maxlen))[0]]
            except Exception as e:
                raise

            ner = ner[-sent_len:]
            
            ner = self.transformer.to_ner(ner, self.ner_dict)
            
            segment.append(words)
            part_of_speach.append(tags[0])
            result.append(ner)

        return segment, part_of_speach, result 
    
    def predict_qa_test(self, data):
        sentence = self.TextProcessor.sentence_break(data, split_char='!?。！？,，」"')
        # sentence = list(data)
        segment = []
        part_of_speach = []
        result = []
        words_list, tags_list = self.TextProcessor.seg_tag(sentence, use_stopwords=False)
        for i in range(len(words_list)):
            words = words_list[i]
            tags = tags_list[i]

            sent_len = len(words)

            pos = self.transformer.to_int([tags], self.pos_dict)##

            pos_pad = self.transformer.padding(pos, maxlen=self.maxlen, padding='pre')
            try:
                ner = [np.argmax(i) for i in self.model.predict(pos_pad.reshape(1,self.maxlen))[0]]
            except Exception as e:
                raise

            ner = ner[-sent_len:]
            
            ner = self.transformer.to_ner(ner, self.ner_dict)
            
            segment.append(words)
            part_of_speach.append(tags)
            result.append(ner)
        return segment, part_of_speach, result 
    
    def predict_qa_train(self, data):#一次丟100句
        # sentence = self.TextProcessor.sentence_break(data, split_char='!?。！？,，」"')
        sentence = list(data)
        segment = []
        part_of_speach = []
        result = []
        words_list, tags_list = self.TextProcessor.seg_tag(sentence, use_stopwords=False)
        for i in range(len(words_list)):
            words = words_list[i]
            tags = tags_list[i]

            sent_len = len(words)

            pos = self.transformer.to_int([tags], self.pos_dict)##

            pos_pad = self.transformer.padding(pos, maxlen=self.maxlen, padding='pre')
            try:
                ner = [np.argmax(i) for i in self.model.predict(pos_pad.reshape(1,self.maxlen))[0]]
            except Exception as e:
                raise

            ner = ner[-sent_len:]
            
            ner = self.transformer.to_ner(ner, self.ner_dict)
            
            segment.append(words)
            part_of_speach.append(tags)
            result.append(ner)
        return segment, part_of_speach, result 

class data_trans():
    def __init__(self):
        pass

    def load_data_csv(self, path):
        with open(path,'r', encoding='utf-8-sig') as f:
            data = csv.reader(f)
            rows = [row for row in data]
        return rows

    def padding(self, X, maxlen, padding='pre'):
        return pad_sequences(X, maxlen=maxlen, padding=padding)

    def to_int(self, X, t_dict):
        X_int = []
        for row in X:
            temp_int = []
            for element in row:
                temp_int.append(t_dict[element])
            X_int.append(temp_int)
        return X_int

    def to_onehot(self, X, t_dict):
        X_onehot = []
        for row in X:
            temp_onehot = []
            for element in row:
                zeros = [0]*len(t_dict)
                zeros[element] = 1
                temp_onehot.append(zeros)
            X_onehot.append(temp_onehot)
        return np.array(X_onehot)

    def to_ner(self, X, t_dict):
        X_ner = []
        for x in X:
            for key, value in t_dict.items():
                if  x == value:
                    X_ner.append(key)
        
        return X_ner

if __name__ == '__main__':
    ner = NER(maxlen=30)
    # dt =  data_trans()
    # data = dt.load_data_csv('data_alex/seg2000_prepare2.csv')
    # pos, tags = [], []
    # for seg in data:
    #     temp_p, temp_t = [],[]
    #     for element in seg:
    #         temp = element.split('%2F')
    #         temp_p.append(temp[1])
    #         temp_t.append(temp[2])
    #     pos.append(temp_p)
    #     tags.append(temp_t)
    # pos = dt.to_int(pos,ner.pos_dict)
    # pos_pad = dt.padding(pos, maxlen=ner.maxlen, padding='pre')
    # tags = dt.to_int(tags, ner.ner_dict)
    # tags_pad = dt.padding(tags, maxlen=ner.maxlen, padding='pre')
    # tags_onehot = dt.to_onehot(tags_pad, ner.ner_dict)

    # ner.build_model(ner.maxlen, len(ner.pos_dict), len(ner.ner_dict), 32, 16)
    # ner.train(pos_pad, tags_onehot, batch_size=10, epochs=5, validation_split=0.2)

    text = '明天是小方的生日，小方打電話給小亮。小方說：「小亮，明天是我生日，請你來我家好嗎？」小亮說：「好啊！我會唱歌給你聽。」小方說：「你要唱什麼歌？」小亮說：「我明天再告訴你。」小方說：「好啊！你明天一定要來！」'

    segment, pos, text_ner = ner.predict(text)
    print("原文:", text)
    print("斷詞:", segment)
    print("實體辨識:", text_ner)

    # ner.save_model('/model/ner_init/ner_model.h5')