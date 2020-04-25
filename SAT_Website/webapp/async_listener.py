import django

django.setup()
from .streamlistener import listen
from .ModelTraining.NuancedSentimentDetection.AnalyzeSentiment import get_sentiment
from .models import Tweets, Tags, Terms
import os
import signal
from random import randint


# taken from stackoverflow to kill rouge hanging processes
class TimeoutException(Exception):  # Custom exception class
    pass


def TimeoutHandler(signum, frame):  # Custom signal handler
    raise TimeoutException


def start_listener(*args):
    # wait 12 minutes for listener

    """
    try:
        OriginalHandler = signal.signal(signal.SIGALRM, TimeoutHandler)
    except AttributeError:
        pass
    """
    pid = os.getpid()
    args = list(args)
    search_year = args.pop()
    term_id = args.pop()
    tweets = []

    print("Executing in thread with pid:", pid)
    # signal.alarm(720)

    if search_year == '2020':

        print("Starting listener...")
        listener = listen(200, args)
            # crappy loop, gets the job done.
            # from our generator we receive tweet objects for sorting and collection
        while True:
            try:
                if listener.done:
                    for tweet in listener.get_tweets():
                        tweet.text = tweet.text.replace('\n', ' ')
                        tweets.append(tweet.text)
                        new_tweet = Tweets(text=tweet.text, year=tweet.year)
                        new_tweet.save(using='tweets')
                        if tweet.hashtags:
                            # some tweets were failing because of unicode characters, added in to continue exec
                            try:
                                tweet_id = Tweets.objects.using('tweets').all().filter(text__iexact=tweet.text,
                                                                                       year=tweet.year)
                                tweet_id[0]
                            except IndexError:
                                # print(tweet.text)
                                continue
                            for tag in tweet.hashtags:
                                new_tag = Tags(id=tweet_id[0], hashtag=tag)
                                new_tag.save(using='tweets')
                    break
            except TimeoutException:
                term = Terms.objects.using('tweets').get(id=term_id)
                term.delete(using='tweets')
                print("Timed out. Killing process", pid)
                # signal.alarm(0)
                # signal.signal(signal.SIGALRM, OriginalHandler)
                # os.kill(pid, 9)

    # Reset the alarm stuff, execute code if query is for previous years
    else:
        # signal.alarm(0)
        # signal.signal(signal.SIGALRM, OriginalHandler)
        query = ' '.join(args)
        print("Year:", search_year + ".", "Running get_sentiments() with database for query:", query)
        tweet_db = Tweets.objects.using('tweets').all().filter(text__icontains=query, year=search_year)
        for item in tweet_db:
            tweets.append(str(item.text))

    # save sentiment value for collection of tweets
    print("Analysing...")
    rand = randint(0, len(tweets))
    # print(tweets)
    positivity, sentiment = get_sentiment(tweets)
    sentiment = str(sentiment)
    sentiment = ''.join(sentiment)
    print("Finished analysing, saving results...")
    term = Terms.objects.using('tweets').get(id=term_id)
    term.positivity = positivity
    term.sentiment = sentiment
    term.r_tweet = tweets[rand]
    term.save(using='tweets')


