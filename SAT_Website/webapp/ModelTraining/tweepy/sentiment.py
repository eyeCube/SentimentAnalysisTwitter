'''
    
'''

import sys
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# import twitter keys and tokens
from config import *

class Global:
    # constants
    __TRAINING__=0

class TrainingData:
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            self.__dict__[k] = v

class TweetStreamListener(StreamListener):
    __IMPORTED_TEXTBLOB__=False
    __IMPORTED_ELASTICSEARCH__=False

    def __init__(self, *args, **kwargs):
        super(TweetStreamListener, self).__init__(args, kwargs)

        self.es=None
        self.trainingdata=[]
    
    @classmethod
    def import_textBlob(cls):
        from textblob import TextBlob
        __IMPORTED_TEXTBLOB__=True
    @classmethod
    def import_elasticSearch(cls):
        from elasticsearch import Elasticsearch
        # create instance of elasticsearch
        self.es = Elasticsearch()
        __IMPORTED_ELASTICSEARCH__=True
    
    # on success
    def on_data(self, data):

        if Global.__TRAINING__:
            self.on_data_train(data)
            return
        
        # decode json
        decoded = json.loads(data)
        
        return interpret(decoded)

    def on_data_train(self, data):
        '''
            we can use TextBlob to produce training data for the 
            machine learning model. 
        '''
        
        # decode json
        decoded = json.loads(data)
        
        return interpret_textblob(decoded)
        
    def interpret_textblob(self, data):
        if not TweetStreamListener.__IMPORTED_TEXTBLOB__:
            TweetStreamListener.import_textBlob()
        if not TweetStreamListener.__IMPORTED_ELASTICSEARCH__:
            TweetStreamListener.import_elasticSearch()
        
        # pass tweet into TextBlob
        tweet = TextBlob(data["text"])
        
        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"
        
        # output sentiment
        self.trainingdata.append(TrainingData(
            message=data["text"],
            polarity=tweet.sentiment.polarity,
            subjectivity=tweet.sentiment.subjectivity,
            ))
        
        # add text and sentiment info to elasticsearch
        if self.es:
            self.es.index(index="sentiment",
                doc_type="test-type",
                body={"author": data["user"]["screen_name"],
                      "date": data["created_at"],
                      "message": data["text"],
                      "polarity": tweet.sentiment.polarity,
                      "subjectivity": tweet.sentiment.subjectivity,
                      "sentiment": sentiment})
        return True
    # end def
    
    # on failure
    def on_error(self, status):
        print(status)
    # end def

    def write_training_data(self, filename):
        with open(filename, "w") as f:
            for data in self.trainingdata:
                # what format should we use?
                f.write(
                    '''"message":{}
"polarity":{}
'''.format(data.message, data.polarity)
                    )
    # end def
# end class

def main():
    Global.__TRAINING__ = True #TEMPORARY
    # program parameters
##    if len(sys.argv) == 1:
##        printhelp()
##    Global.__TRAINING__ = sys.argv[1]
        
    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()
    
    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    # create instance of the tweepy stream
    stream = Stream(auth, listener)
    
    # filter by the keywords specified in the command line arguments
##    kws=[]
##    for arg in sys.argv[2:]:
##        print(arg)
##        kws.append(arg)
##    
##    stream.filter(track=kws)
    stream.filter(track=['impeach']) #TEMPORARY
#end def

def printhelp():
    print('''Use:
sentiment.py __TRAINING__ args...
 - __TRAINING__ is 0 or 1; if 1, enables training mode.
 - args are a space-delimited list of arguments that are passed as keywords into the stream filter.''')
    
if __name__ == '__main__':
    main()

