import django

django.setup()
from .streamlistener import listen
from .ModelTraining.NuancedSentimentDetection.AnalyzeSentiment import get_sentiment
from .models import Tweets, Tags, Terms
import os


def start_listener(*args):
    args = list(args)
    term_id = args.pop()
    tweets = []
    listener = listen(100, args)
    print("Starting listener...")

    # crappy loop, gets the job done.
    # from our generator we receive tweet objects for sorting and collection
    while True:
        if listener.done:
            for tweet in listener.get_tweets():
                tweet.text = tweet.text.replace('\n', ' ')
                tweets.append(tweet.text)
                new_tweet = Tweets(text=tweet.text, year=tweet.year)
                new_tweet.save(using='tweets')
                if tweet.hashtags:
                    # some tweets were failing because of unicode characters, added in to continue exec
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

    # save sentiment value for collection of tweets
    print("Analysing...")
    positivity, sentiment = get_sentiment(tweets)
    print("Finished analysing, saving results...")
    term = Terms.objects.using('tweets').get(id=term_id)
    term.positivity = positivity
    term.sentiment = sentiment
    term.save(using='tweets')
