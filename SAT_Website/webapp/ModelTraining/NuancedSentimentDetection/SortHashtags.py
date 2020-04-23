from ModelTraining.machinegym import angry, happy, peaceful, sad
import pandas as pd

hashtag_dict = dict(angry=angry.HASHTAGS, happy=happy.HASHTAGS, peaceful=peaceful.HASHTAGS, sad=sad.HASHTAGS)
series = []
for key, val in hashtag_dict.items():
    val = val.replace('#', '')
    series.append(pd.Series(val.split(' '), name=key))
df = pd.concat(series, axis=1)
df.to_csv('hashtags.csv')
