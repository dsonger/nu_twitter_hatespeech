from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, Input, LSTM
from keras.models import Sequential, Model, model_from_json
from gensim.parsing.preprocessing import STOPWORDS
from string import punctuation
from my_tokenizer import glove_tokenize

import json
import sys
import pdb
import numpy as np

class TwitterHateClassifier():
    MAX_SEQUENCE_LENGTH = 28
    VOCAB = {}
    MODEL = None
    Y_MAP = {0: 'none', 1: 'racism', 2: 'sexism'}
    
    def __init__(self):
        self.VOCAB = self.__load_vocab()
        self.MODEL = self.__load_model()
    
    def __load_vocab(self):
        with open("lstm_vocab.json", 'rb') as vocab_file:
            return json.loads(vocab_file.readline())

    def __gen_sequence(self, raw_tweet):
        text = glove_tokenize(raw_tweet['text'].lower())
        text = ' '.join([c for c in text if c not in punctuation])
        words = text.split()
        words = [word for word in words if word not in STOPWORDS]
        seq = []
        for word in words:
            seq.append(self.VOCAB.get(word, self.VOCAB['UNK']))
        return seq

    def __load_model(self):
        # load json and create model
        json_file = open('lstm_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("lstm_model.h5")
        print("Loaded model LSTM classifier from disk...\n")
        return loaded_model

    def __get_data(self, raw_tweet):
        seq = self.__gen_sequence(raw_tweet)
        return pad_sequences([seq], maxlen=self.MAX_SEQUENCE_LENGTH)

    def predict(self, raw_tweet):
        data = self.__get_data(raw_tweet)
        y_pred = self.MODEL.predict(data)
        y_val = np.argmax(y_pred, axis=1)
        y_val = y_val[0]
        return self.Y_MAP[y_val]

if __name__ == "__main__":
    sample_tweet = {
        "text": "so my sister dyed her hair today. There was some left over dye, so what do I do? I dyed the blonde part of my hair blue.", 
        "user": {"name": "Vile_Islam"}, 
        "id": 552247283438587905, 
        "Annotation": "racism"
    }
    
    hate_classifier = TwitterHateClassifier()
    print("PREDICTION: ", hate_classifier.predict(sample_tweet))
    

