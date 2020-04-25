# Create the Naive Bayes model for predicting hashtag category
# Author: Oscar Kosar-Kosarewicz

from sklearn.naive_bayes import MultinomialNB
from pickle import dump
from scipy import sparse
import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
import os
import pandas as pd
import json
from ..machinegym.machinegym import score_by_dataframe
import pickle
from .AnalyzeSentiment import predict_NB


def filter_tweets():
    data = pd.DataFrame()
    hashtags = pd.read_csv('hashtags.csv')
    for i in range(4):
        dir = f'C:\\Users\\okosa\\Desktop\\Tweets{i}\\'
        for file_name in os.listdir(dir):
            if file_name.endswith('.json.txt'):
                with open(os.path.join(dir, file_name)) as f:
                    tweets = json.load(f)
                tweets = pd.DataFrame(tweets['tweets'])
                for tweet in tweets.iterrows():
                    tags = [x.lower() for x in tweet[1][1]]
                    if pd.Series(tags).isin(hashtags.to_numpy().flatten()).any():
                        for i in range(8):
                            if pd.Series(tags).isin(hashtags.T.to_numpy()[i]).any():
                                category = i
                        entry = pd.DataFrame([tweet[1]], columns=['text', 'hashtag', 'year'])
                        entry['category'] = category
                        data = data.append(entry)

    data.reset_index(drop=True, inplace=True)

    data[['text', 'category']].to_csv('NB_training_data.csv', index=False)
    data = score_by_dataframe(pd.DataFrame(data['text']))
    data.to_csv('text.csv', index=False)
    print(data)



def prep_data_for_LR(data):
    mg_data = score_by_dataframe(data)

if __name__ == '__main__':
    filter_tweets()
    data = pd.read_csv('NB_training_data.csv')
    prediction = predict_NB(data['text'])
    prediction2 = score_by_dataframe(pd.DataFrame(data['text']))
    prediction.reset_index(drop=True, inplace=True)
    prediction2.reset_index(drop=True, inplace=True)
    ggg = pd.concat([prediction2, prediction], axis=1)
    ggg.to_csv('test.csv')
