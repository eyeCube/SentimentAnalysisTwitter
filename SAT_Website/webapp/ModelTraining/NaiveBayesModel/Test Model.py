# Test the NB model
# Author: Oscar Kosar-Kosarewicz

import pandas as pd
import sklearn
import pickle
import numpy as np

DIR = r'./'
infile = DIR + 'validation_data.npy'
model_path = 'NB.pickle'
vectorizer_path = 'vectorizer.pickle'

with open(model_path, 'rb') as f:
    model = pickle.load(f)
with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

test_data = np.load(infile, allow_pickle=True)
processed_data = vectorizer.transform(test_data[:, 0])
result = model.score(processed_data, test_data[:, 1].astype('int'))
print(result)

