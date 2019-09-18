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
    def __init__(self, model_path = cwd+'/data_alex/ner_model.h5',
                    posDict_path = cwd+'/data_alex/pos_dict.txt',
                    nerDict_path = cwd+'/data_alex/ner_dict.txt'):
        try:
            self.model = load_model(model_path)
        except:
            self.model = None
        
        with open(posDict_path) as f: self.pos_dict = json.load(f)
        with open(nerDict_path) as f: self.ner_dict = json.load(f)

        self.TextProcessor = TextProcessor.TextProcessor()
        self.transformer = data_trans()
        self.maxlen = 30

    def print_path(self):
        return cwd2
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

    def train(self, X, Y, batch_size=1, epochs=1, validation_split=0.2):
        self.model.fit(X, Y, batch_size=batch_size, epochs=epochs, validation_split=validation_split)

    def save_model(self, path):
        self.model.save(path)

    def predict(self, data):
        sentence = self.TextProcessor.sentence_break(data, split_char='!?。！？,，')

        if not self.model:
            model = _load_model(cwd+'/data_alex/ner_model.h5')

        segment = []
        part_of_speach = []
        result = []
        for sent in sentence:
            words, tags = self.TextProcessor.seg_tag(sent, use_stopwords=False)
            words = words[0]

            sent_len = len(words)

            pos = self.transformer.to_int(tags, self.pos_dict)

            pos_pad = self.transformer.padding(pos, maxlen=self.maxlen, padding='pre')
            
            ner = [np.argmax(i) for i in self.model.predict(pos_pad.reshape(1,self.maxlen))[0]]
            ner = ner[-sent_len:]
            
            ner = self.transformer.to_ner(ner, self.ner_dict)
            
            segment.extend(words)
            part_of_speach.extend(tags[0])
            result.extend(ner)

        return segment, part_of_speach, result 

class data_trans():
    def __init__(self):
        pass

    def _load_data_csv(self, path):
        with open(path,'r',encoding='utf-8-sig') as f:
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
    text = '小狗，小狗跟我來，我們比一比，看誰跑得快？'

    ner = NER()
    segment, pos, text_ner = ner.predict(text)
    print(segment)
    print(pos)
    print(text_ner)