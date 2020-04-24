import pandas as pd
import pickle
import numpy as np
from ModelTraining.machinegym.machinegym import score_by_dataframe
from os import path
from ModelTraining.NaiveBayesModel.PredictSentiment import predict_sentiment
from sklearn.preprocessing import normalize

sentiments = {
    0:'angry',
    1:'happy',
    2:'peaceful',
    3:'sad',
    4:'fear',
    5:'fun',
    6:'safe',
    7:'bored'
}

normlization_values =[0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 7.41499385e-02,
 3.32240885e-01, 4.09668169e-04, 5.91151168e-01, 2.04834084e-03]

# get tweet sentiment
# input: sequence of tweets
# output: percentage of positive tweets, most common emotion
def get_sentiment(tweets):
    model_path = path.join(path.dirname(__file__), 'LR.pickle')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    machine_gym_score = score_by_dataframe(pd.DataFrame(tweets))
    tweets = tweets.str.lower()  # make the tweets all lowercase
    tweets.replace(regex=True, inplace=True, to_replace=r'[^a-z\s]',
                 value='')  # Remove punctuation and numbers from tweets
    NB_score = predict_NB(tweets)
    NB_score.reset_index(drop=True, inplace=True)
    machine_gym_score.reset_index(drop=True, inplace=True)
    predictors = pd.concat([NB_score, machine_gym_score.iloc[:,1:]], axis=1)
    results = model.predict(predictors)
    results = np.subtract(np.divide(np.bincount(results), np.sum(np.bincount(results))), normlization_values)
    most_frequent = np.argmax(results)
    print(results)
    print(most_frequent)

    rating = predict_sentiment(tweets)
    rating = np.asarray(np.unique(rating, return_counts=True))
    percentage_positive = rating[1, 1] / np.sum(rating[1,:])
    return percentage_positive, sentiments[most_frequent]

def predict_NB(data):
    model_path = path.join(path.dirname(__file__), 'NB_model.pickle')
    vectorizer_path = path.join(path.dirname(__file__), 'vectorizer.pickle')
    with open(model_path, 'rb') as f:
        modelNB = pickle.load(f)
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)

    tweets = data
    tweets = vectorizer.transform(tweets)

    prediction = modelNB.predict(tweets)
    result = np.zeros([prediction.shape[0], 8])
    for i, score in enumerate(prediction):
        result[i, score] = 1
    return pd.DataFrame(result)

if __name__ == '__main__':
   tweets = pd.read_csv('text.csv')['text']
   results = get_sentiment(tweets)
   print(results)