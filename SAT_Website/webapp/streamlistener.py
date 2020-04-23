'''
    streamlistener.py
    author: Jacob Wharton
    
    This is a Tweepy StreamListener implementation that collects tweets
    into a list of Tweet objects.
    
    You can run this module in two ways:
    1. import streamlistener.py and run listen()
    2. run this file from the command line.
        * get_tweets() (& print_tweets()) may be useful for this
'''

'''
    required:
        pip install tweepy
'''


import pycld2
import os # environment vars
import sys # console args
import json # tweepy stream data decoding
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import textblob

from .ModelTraining.machinegym import machinegym
### import machinegym from relative path (if not in same directory):
##import importlib.util
##spec = importlib.util.spec_from_file_location("machinegym.py", "../machinegym/machinegym.py")
##machinegym = importlib.util.module_from_spec(spec)
##spec.loader.exec_module(machinegym)

# constants
API_KEY     = os.environ['API_KEY']
API_SECRET  = os.environ['API_SECRET']
ACCESS_TOKEN= os.environ['ACCESS_TOKEN']
TOKEN_SECRET= os.environ['TOKEN_SECRET']


def extract_hashtags(text: str) -> set: # get words beginning with '#' (hashtags)
    split=[]
    temp=[]
    for i in text.split('\n'):
        temp.append(i)
    for j in temp:
        for i in j.split(' '):
            split.append(i)
    return set(part[1:] for part in split if part.startswith('#'))


# global variables stored here
class Global:
    __TRAINING__=0 # are we in training mode?

class TrainingData: # data struct for machine learning training data
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            self.__dict__[k] = v
            
class Tweet: # data struct for storing individual tweet data
    __slots__=['text','hashtags','year']
    def __init__(self, text:str, hashtags:set, year:int):
        self.text=text
        self.hashtags=hashtags
        self.year=year
    def __repr__(self):
        return {'text':self.text,'hashtags':self.hashtags,'year':self.year}
    def __str__(self):
        return 'Tweet(text={}, hashtags={}, year={})'.format(self.text,self.hashtags,self.year)

# Tweet Listener: collects tweets from Twitter API using tweepy
class TweetStreamListener(StreamListener):
    __IMPORTED_TEXTBLOB__=False
    __IMPORTED_ELASTICSEARCH__=False

    def __init__(self, maximum:int):
        '''
            Parameters:
                maximum - max number of tweets to collect
        '''
        super(TweetStreamListener, self).__init__()
        
        self.maximum=maximum # max number of tweets to collect
        self.es=None
        self.trainingdata=[]
        self.tweets=[]
        self.exit_on_error=True # stop stream if an error occurs in collecting tweets?
        self.done=False
        
    def add_tweet(self, text:str, hashtags:set, year:int):
        self.tweets.append(Tweet(text,hashtags,year))
    
    # generator to get the list of Tweet objects
    def get_tweets(self):
        for tweet in self.tweets:
            yield tweet
    
    # simply print the received tweets to the console
    def print_tweets(self):
        for tweet in self.get_tweets():
            print(tweet)
    
    # on success: StreamListener function
    def on_data(self, data) -> bool:
        '''
            function is called when a tweet is received by the Tweepy Listener.
            Parameters:
                data represents a tweepy tweet data object
            Returns True to continue the stream, or False to stop the stream.
        '''
        
        if len(self.tweets) >= self.maximum:
            print("Finished collecting tweets after {} collected.".format(self.maximum))
            self.done = True
            return False
        
        if Global.__TRAINING__:
            self.on_data_train(data)
            return True
        
        # decode json
        decoded = json.loads(data)
        
        return self.interpret_textblob(decoded)
    # end def
    
    # on failure: StreamListener function
    def on_error(self, status) -> bool:
        ''' like on_data but for failure / error state '''
        print("Error: ", status)
        if self.exit_on_error:
            return False # stop the stream
        return True

    def on_data_train(self, data) -> bool:
        '''
            we can use TextBlob to produce training data for the 
            machine learning model. 
        '''
        
        # decode json
        decoded = json.loads(data)
        
        return interpret_textblob(decoded)
    # end def

    def interpret_training(self, data):
        
        # output sentiment
        self.trainingdata.append(TrainingData(
            message=data["text"],
            polarity=tweet.sentiment.polarity,
            subjectivity=tweet.sentiment.subjectivity,
            ))
        
        # add relevant tweet data to elasticsearch (DO WE NEED ELASTICSEARCH?)
        if self.es:
            self.es.index(index="sentiment",
                doc_type="test-type",
                body={"author": data["user"]["screen_name"],
                      "date": data["created_at"],
                      "message": data["text"],
                      "polarity": tweet.sentiment.polarity,
                      "subjectivity": tweet.sentiment.subjectivity,
                      "sentiment": sentiment})
    # end def
        
    def interpret_textblob(self, data) -> bool:
        if not data.get("text", None):
            return True
        
        # pass tweet into TextBlob
        tweet = textblob.TextBlob(data["text"])

        # add relevant tweet data
        text = data['text']
        hashtags = extract_hashtags(text) # set
        date = data['created_at']
        year = date[-4:]
        yearint = int(year)
        english = is_english(text)

        # test
##        print("year of tweet: ", year)
        
        # add to tweets
        if english:
##            print(text)
##            print(hashtags)
##            print(year)
            self.add_tweet(text, hashtags, yearint)
        
        return True
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

def is_english(text:str):
    data=pycld2.detect(text, isPlainText=True)
    if data[0]==False:
        return False
    if (data[2][0][1]=="en"
    and data[2][0][2]>=95):
        return True
    return False

def listen(maximum_tweets:int, *args):
    '''
        primary function: Initialize a TweetStreamListener object, collect
        tweets up to a maximum amount matching the keywords given, and return
        those tweets.
        Parameters:
            maximum_tweets - max number of tweets to collect before stopping
            args - listens for tweets matching the keywords specified in *args
        Returns: tweets matching those keywords
    '''
    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener(int(maximum_tweets))
    
    # set twitter API keys/tokens to initialize the stream listener
    # API key
        # consumer key, consumer secret
    auth = OAuthHandler(
        API_KEY,        # just hard-code the public keys
        API_SECRET      # twitter API secret keys stored as ...
        )               # ... environment variables on the server
    # access token
        # access token, access secret
    auth.set_access_token(
        ACCESS_TOKEN,
        TOKEN_SECRET
        )
    
    # create instance of the tweepy stream to listen for tweets
    stream = Stream(auth, listener)
    
    # filter by the keywords specified in the command line arguments
    stream.filter(track=[arg[0] for arg in args], is_async=True) # asynchronous: run on separate thread
    return listener
#end def

def main():
    # program parameters
    if len(sys.argv) <= 2:
        printhelp()
        return
    listener = listen(sys.argv[1], sys.argv[2:])
    while True:
        if listener.done:
            listener.print_tweets()
            break

def printhelp():
    print('''To use, run:
python3 streamlistener.py maximum_tweets args
 - maximum_tweets is an integer representing max number of tweets to collect.
 - args: space-delimited list of keywords that are passed into stream filter.''')
    
if __name__ == '__main__':
    main()

