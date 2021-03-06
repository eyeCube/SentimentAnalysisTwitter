# Oscar Kosar-Kosarewicz
# Creates an SGD Regression machine learning using Amazon reviews and pickles it
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDRegressor
import pickle

DIR = r'C:/Users/okosa/Desktop/'
infile = DIR + 'training data.csv'
#outfile = DIR + 'SGD'

# read in data from csv in chunks
chunks = pd.read_csv(infile, chunksize=4000)
vectorizer = HashingVectorizer(2 ** 20)  # converts strings of text into vectors of word counts

# save vectorizer to file
with open('vectorizer.pickle', 'wb') as f:
    pickle.dump(vectorizer, f)

sgd = SGDRegressor()  # The ML model
for chunk in chunks:
    vectorized = vectorizer.transform(chunk['review_body'].values.astype('U'))
    sgd.partial_fit(vectorized, chunk['star_rating'])

# save model to file
with open('SGD.pickle', 'wb') as f:
    pickle.dump(sgd, f)

