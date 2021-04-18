import csv
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.layers import LSTM, GRU,Bidirectional, Flatten, Dense
from keras_self_attention import SeqSelfAttention
import csv, re
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
from keras import optimizers
import numpy as np
from keras.preprocessing.text import  Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import  EarlyStopping, ModelCheckpoint
from keras_self_attention import SeqSelfAttention, SeqWeightedAttention

dict_intent = {'build_item':0,
'support_socket':1,
'counter':2,
'be_countered':3,
'skill_up':4,
'how_to_play':5,
'combo':6,
'combine_with':7,
'how_to_use_skill':8,
'introduce':9
}
dict_digit2intent = {}
key = 0
for i in dict_intent.keys():
    dict_digit2intent[key] = i
    key += 1
f = open('./Crawl_data/champions.txt', "r")
reg = ""
for cham in f:
    # print (cham.split ('\n')[0])
    reg += cham.split ('\n')[0] + '|'
    # print (reg)
reg = reg[:-1]
skills = ['q', 'w', 'e' , 'r']
def get_entity(content): 
    content = content.lower()
    hero = re.search(reg, content)
    if hero != None:
        hero = hero.group()
    else: hero = ""
    spl = content.split(" ")
    skill = ""
    for i in spl:
        if i in skills:
            skill = i
            break
    return hero, skill
def load_model():
    model = Sequential()
    model.add(Embedding(208, 5248, input_length=17))
    model.add(Bidirectional(LSTM(128, return_sequences=True)))
    #model.add(LSTM(128, return_sequences = True))
    model.add(Flatten())
    # checkpoint = ModelCheckpoint('/home/vanhocvp/Code/AI/NLP/API/model1.h5', verbose=1, monitor='val_loss',save_best_only=True, mode='auto')
    model.add(Dense(10, activation='softmax'))
    model.compile(loss= 'categorical_crossentropy',optimizer='adam', metrics=['accuracy'])
    model.load_weights('model4.h5')
    model.summary()
    return model
def process_content(reg, content): 
    content = content.lower()
    x = re.search(reg, content)
    
    if x != None:
        content = content.replace(x.group(), "{hero}")
    return content
def process_data(model, content):
    # content = process_content(reg, content)
    f = open('./data/vocab1.txt', 'r')
    dictionary = ''
    for word in f:
        dictionary += word + " "
    f.close()
    data = [dictionary]
    token_obj = Tokenizer()
    token_obj.fit_on_texts(data)
    max_len = 17
    # vocab_size = 208
    X_train_token = token_obj.texts_to_sequences([content])
    X_pad = pad_sequences(X_train_token, maxlen=max_len, padding='post')
    # print (content)
    # print (X_pad.shape)

    result = model.predict(X_pad)
    intent = np.argmax(result)
    hero, skill = get_entity(content)
    # print(hero)
    # print (skill)
    # print((result.shape))
    return dict_digit2intent[intent], result[0][intent], hero, skill

