from sklearn.naive_bayes import MultinomialNB
from pickle import dump
from scipy import sparse
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer

training_data = np.load('training_data.npy', allow_pickle=True)
validation_data = np.load('validation_data.npy', allow_pickle=True)


model = MultinomialNB()
vectorizer = HashingVectorizer(2**20, strip_accents='unicode', norm=None, alternate_sign=False)
x = vectorizer.transform(training_data[:, 0])
y =  training_data[:, 1].astype('int')

model.fit(x, y)

with open('vectorizer.pickle', 'wb') as f:
    dump(vectorizer, f)
with open('NB.pickle', 'wb') as f:
    dump(model, f)

x = vectorizer.transform(validation_data[:, 0])
y = validation_data[:, 1].astype('int')
print(model.score(x, y))
