# Test the NB model
# Author: Oscar Kosar-Kosarewicz

import pandas as pd
import sklearn
import pickle
import numpy as np

DIR = r'./'
infile = DIR + 'NB_training_data.csv'
infile = DIR + 'test.csv'
model_path = 'test_model.pickle'
model_path = 'LR.pickle'
vectorizer_path = 'test_vectorizer.pickle'

with open(model_path, 'rb') as f:
    model = pickle.load(f)
with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

#test_data = pd.read_csv(infile).to_numpy()
#processed_data = vectorizer.transform(test_data[:, 0])
#result = model.score(processed_data, test_data[:, 1].astype('int'))
x = pd.read_csv(infile).to_numpy()[:,2:]
y = pd.read_csv('NB_training_data.csv')['category']
result = model.score(x, y)
predictions = model.predict(x)

print(result)

