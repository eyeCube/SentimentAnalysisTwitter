import pandas as pd
import sklearn
import pickle

DIR = r'C:/Users/okosa/Desktop/'
infile = DIR + 'test_data.csv'
model_path = 'SGD.pickle'
vectorizer_path = 'vectorizer.pickle'

with open(model_path, 'rb') as f:
    model = pickle.load(f)
with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

test_data = pd.read_csv(infile)
processed_data = vectorizer.transform(test_data['review_body'].values.astype('U'))
result = model.score(processed_data, test_data['star_rating'])
print (result)
