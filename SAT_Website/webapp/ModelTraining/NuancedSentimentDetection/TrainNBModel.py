from ..NaiveBayesModel.CreateModel import create_model
import pandas as pd
import pickle

training_data = pd.read_csv('NB_training_data.csv')
training_data['text'] = training_data['text'].str.lower()  # make the tweets all lowercase
training_data['text'].replace(regex=True, inplace=True, to_replace=r'[^a-z\s]',
                     value='')  # Remove punctuation and numbers from tweets
model, vectorizer = create_model(training_data)

with open('NB_model.pickle', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pickle', 'wb') as f:
    pickle.dump(vectorizer, f)
