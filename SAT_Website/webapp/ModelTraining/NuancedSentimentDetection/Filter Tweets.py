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

dir = r'C:\Users\okosa\Desktop\Tweets\\'
dir1 = r'C:\Users\okosa\Desktop\Tweets1\\'
data = pd.DataFrame()
#TODO ignore case in hashtags

hashtags = pd.read_csv('hashtags.csv')
for file_name in os.listdir(dir) + os.listdir(dir1):
    if file_name.endswith('.json.txt'):
        with open(os.path.join(dir, file_name)) as f:
            tweets = json.load(f)
        tweets = pd.DataFrame(tweets['tweets'])
        for tweet in tweets.iterrows():
            tags = [x.lower() for x in tweet[1][1]]
            if pd.Series(tags).isin(hashtags.to_numpy().flatten()).any():
                if pd.Series(tags).isin(hashtags.T.to_numpy()[0]).any():
                    category = 'angry'
                elif pd.Series(tags).isin(hashtags.T.to_numpy()[1]).any():
                    category = 'happy'
                elif pd.Series(tags).isin(hashtags.T.to_numpy()[2]).any():
                    category = 'peaceful'
                elif pd.Series(tags).isin(hashtags.T.to_numpy()[3]).any():
                    category = 'sad'
                entry = pd.DataFrame([tweet[1]], columns=['text', 'hashtag', 'year'])
                entry['category'] = category
                data = data.append(entry)
data.to_csv('text.csv')
data[['text', 'category']].to_csv('training_data.csv')


