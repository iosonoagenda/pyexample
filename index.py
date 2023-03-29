import numpy as np
import pandas as pd
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout
from keras.models import Model
from keras import backend as K
from sklearn.model_selection import train_test_split

# load data from CSV file
data = pd.read_csv('tweets.csv')

# preprocess the data (remove special characters, lowercase, tokenize)
tokenizer = Tokenizer(num_words=10000, split=' ')
tokenizer.fit_on_texts(data['tweet'].values)
X = tokenizer.texts_to_sequences(data['tweet'].values)
X = pad_sequences(X)

# create train and test sets
Y = pd.get_dummies(data['label']).values
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.20, random_state = 42)

# build LSTM-based neural network model for sentiment analysis
inputs = Input(shape=(X_train.shape[1],))
embedding_layer = Embedding(10000, 128)(inputs)
lstm_layer = LSTM(196)(embedding_layer)
dropout_layer = Dropout(0.2)(lstm_layer)
dense_layer = Dense(2, activation='softmax')(dropout_layer)
model = Model(inputs, dense_layer)

# compile and fit the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, Y_train, epochs=10, batch_size=32, validation_data=(X_test, Y_test))

# evaluate the model on test data
loss, accuracy = model.evaluate(X_test, Y_test, verbose=False)
print(f'Test Accuracy: {accuracy:.4f}')