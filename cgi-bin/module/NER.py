# coding: utf-8
from keras.models import Sequential
from keras.layers import Dense, LSTM, InputLayer, Bidirectional, TimeDistributed, Embedding, Activation
from keras.optimizers import Adam
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
# from module.TextProcessor import TextProcessor
import TextProcessor
import csv
import numpy as np
import json

class NER():
    def __init__(self, model_path='./data_alex/ner_model.h5', posDict_path='./data_alex/pos_dict.txt', nerDict_path='./data_alex/ner_dict.txt'):
        try:
            self.model = load_model(model_path)
        except:
            self.model = None
        self.data = None
        
        with open(posDict_path) as f:
            self.pos_dict = json.load(f)
        
        with open(nerDict_path) as f:
            self.ner_dict = json.load(f)

        self.transformer = data_trans()
        self.maxlen = 30

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
        processor = TextProcessor.TextProcessor()
        sentence = processor.sentence_break(data, split_char='!?。！？,，')

        if not self.model:
            model = _load_model('data_alex/ner_model.h5')

        segment = []
        result = []
        for sent in sentence:
            words, tags = processor.seg_tag(sent, use_stopwords=False)
            words = words[0]

            sent_len = len(words)

            pos = self.transformer.to_int(tags, self.pos_dict)

            pos_pad = self.transformer.padding(pos, maxlen=self.maxlen, padding='pre')
            
            ner = [np.argmax(i) for i in self.model.predict(pos_pad.reshape(1,self.maxlen))[0]]
            ner = ner[-sent_len:]
            
            ner = self.transformer.to_ner(ner, self.ner_dict)
            
            segment.extend(words)
            result.extend(ner)

        return segment, result

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
    # maxlen = 30
    NER = NER()
    # data = NER.transformer._load_data_csv('./data_alex/seg2000_prepare2.csv')
    # pos, ner = [],[]
    # for row in data:
    #     temp_pos, temp_ner = [],[]
    #     for words in row:
    #         tags = words.split("%2F")
    #         temp_pos.append(tags[1].strip())
    #         temp_ner.append(tags[2].strip())
    #     pos.append(temp_pos)
    #     ner.append(temp_ner)

    # pos = NER.transformer.to_int(pos, NER.pos_dict) 
    # ner = NER.transformer.to_int(ner, NER.ner_dict)

    # pos_X = NER.transformer.padding(pos, maxlen=maxlen, padding='pre')
    # ner_X = NER.transformer.padding(ner, maxlen=maxlen, padding='pre')
    # ner_onehot = NER.transformer.to_onehot(ner_X, NER.ner_dict)
    # ner_onehot = np.array(ner_onehot)

    # input_len = maxlen
    # input_dim = 29
    # output_dim = 7
    # embed_units = 32
    # lstm_units = 64
    # NER.build_model(input_len, input_dim, output_dim, embed_units, lstm_units)
    # NER.train(pos_X, ner_onehot, batch_size=10, epochs=5, validation_split=0.2)
    # NER.save_model('data_alex/ner_model.h5')

    print(NER.predict('小方喜歡同學，同學也喜歡小方。'))
