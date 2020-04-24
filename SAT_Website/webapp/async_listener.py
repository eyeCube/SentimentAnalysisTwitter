import django
django.setup()
from .streamlistener import listen
from .ModelTraining.NuancedSentimentDetection.AnalyzeSentiment import get_sentiment
from .models import Tweets, Tags
import os


def start_listener(*args):
    tweets = []
    listener = listen(100, args)
    print("Starting listener...")

    while True:
        if listener.done:
            for tweet in listener.get_tweets():
                tweet.text = tweet.text.replace('\n', ' ')
                tweets.append(tweet.text)
                new_tweet = Tweets(text=tweet.text, year=tweet.year)
                new_tweet.save(using='tweets')
                if tweet.hashtags:
                    try:
                        tweet_id = Tweets.objects.using('tweets').all().filter(text__iexact=tweet.text, year=tweet.year)
                        tweet_id[0]
                    except IndexError:
                        # print(tweet.text)
                        continue
                    for tag in tweet.hashtags:
                        new_tag = Tags(id=tweet_id[0], hashtag=tag)
                        new_tag.save(using='tweets')
            break

    print("Analysing...")
    print(get_sentiment(tweets))
