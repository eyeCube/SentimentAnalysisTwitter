'''
    machinegym.py
    A module that contains functions for creating training data
    for a machine learning model that analyzes the sentiments in
    a body of text.
'''

''' necessary:
>>>import textblob
>>>import nltk
>>>nltk.download('brown')
>>>nltk.download('punkt')
'''

'''
    TODO:
        tweepy working with machinegym
        more emotions, more words for each emotion
            
        emoticons
        
'''

from textblob import TextBlob, tokenizers
import numpy
import pandas

from ModelTraining.machinegym.meta import *
import ModelTraining.machinegym.happy as happy
import ModelTraining.machinegym.sad as sad
import ModelTraining.machinegym.angry as angry
import ModelTraining.machinegym.peaceful as peaceful
import ModelTraining.machinegym.bored as bored
import ModelTraining.machinegym.fun as fun
from ModelTraining.machinegym.grammar import PREFIX_QUALIFIERS, POSTFIX_QUALIFIERS

class G: # global data stored here
    blob=None
    text=""
    hashtags=set()
# end class

def score_by_dataframe(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    '''
        take a pandas DataFrame of tweets, and return a DataFrame of tweets
            along with sentiment values for each sentiment.
            (Each row is a tweet)
        (DataFrames are like tables or dictionaries: 2D grid w/ rows/cols.)
    '''
    newdf=pandas.DataFrame({}, columns=[ # define the columns for DataFrame
        'text','happy','sad','angry','peaceful','fun','bored','safe','fear',
        ])
    for index, row in dataframe.iterrows(): # convert each tweet
        text = row[0]
        happy = ishappy(text) # get happy sentiment, etc.
        sad = issad(text)
        angry = isangry(text)
        peaceful = ispeaceful(text)
        fun = isfun(text)
        bored = isbored(text)
        safe = issafe(text)
        fear = isafraid(text)
        row = pandas.DataFrame(
            text,happy,sad,angry,peaceful,fun,bored,safe,fear
            )
        newdf.concat(newdf, row) # add row to dataframe
    return newdf

def init():
    ''' call this before running any other scripts. '''
    # add negative ranks
    temp={}
    for k,v in C__RANKTOF.items():
        k = min(C_S, abs(k)) * sign(k)
        temp[-k] = -v
    for k,v in temp.items():
        C__RANKTOF[k] = v

def ranktof(i: int) -> float: # convert C_ const into C__ const
    '''
        get the quality amount for a given integer rank
        (These are values from meta.py used for ranking sentiment-words)
    '''
    ii = min(C_S, abs(i)) * sign(i)
    return C__RANKTOF.get(ii, 0) #math.sqrt(i)
def sign(f: float) -> int: # numerical sign, positive, negative, or 0
    if f < 0: return -1
    if f > 0: return 1
    return 0

def extract_hashtags(text: str) -> set:
    ''' get words beginning with '#' (hashtags) from string text '''
    split=[]
    temp=[]
    for i in text.split('\n'):
        temp.append(i)
    for j in temp:
        for i in j.split(' '):
            split.append(i)
    return set(part[1:] for part in split if part.startswith('#'))

def en_check(blob: TextBlob) -> bool: # is language of text English?
    # NOTE: we are using pycld2 now, this is not needed.
    # Although it uses Google Translate API which is more accurate,
    # it also has a limit on number of requests which is not very high.
    if len(blob) < 3: return False
    return ( blob.detect_language()=='en' )

def test(text: str, _type: str, digital=True):
    ''' test the text 'text' for the sentiment given by the string '_type'.
        Parameters:
            text - string to test the sentiment of
            _type - sentiment type 'happy', 'sad', 'angry', 'peaceful', etc.
            digital - if True, the returned value is either -1, 0, or 1
        Returns a float* from -1 to 1, which indicates how well it matches
            the given sentiment '_type'.
            * If 'digital' is True, the returned value is either -1, 0, or 1.
    '''
    if _type=='happy':
        return ishappy(text, digital=digital)
    if _type=='sad':
        return issad(text, digital=digital)
    if (_type=='angry' or _type=='mad'):
        return isangry(text, digital=digital)
    if (_type=='peaceful' or _type=='peace'):
        return ispeaceful(text, digital=digital)
    if _type=='fun':
        return isfun(text, digital=digital)
    if (_type=='bored' or _type=='boredom'):
        return isbored(text, digital=digital)
    if (_type=='safe' or _type=='safety'):
        return issafe(text, digital=digital)
    if (_type=='fear' or _type=='afraid'):
        return isafraid(text, digital=digital)
    #TODO: other sentiments
# end def

def get_digital(quality): return sign(quality)
def sign(number):
    if number < 0: return -1
    if number > 0: return 1
    return 0


    #------------------#
    #    sentiments    #
    #------------------#

# generic
def sentiment(func):
    '''
        wrapper function to initialize an is_sentiment function
        stupidly sets global variables to the G class because why not
    '''
    def inner(*args, **kwargs):
        text = args[0].lower()
        G.text = text
        G.blob = TextBlob(text)
        G.hashtags = extract_hashtags(text)
        return func(*args, **kwargs)
    return inner

#~~~# specific sentiments: #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# happy
@sentiment
def ishappy(text: str, digital=True) -> float:
    quality = 0
    # try to match words & context to change the disposition
    quality += try_generic_happy()
    quality -= try_generic_sad()
    #
    if digital:
        return get_digital(quality)
    else:
        return quality
# end def

# sad
@sentiment
def issad(text: str, digital=True) -> float:
    quality = 0
    # try to match words & context to change the disposition
    quality -= try_generic_happy()
    quality += try_generic_sad()
    #
    if digital:
        return get_digital(quality)
    else:
        return quality
# end def

# sad
@sentiment
def isangry(text: str, digital=True) -> float:
    quality = 0
    # try to match words & context to change the disposition
    quality -= try_generic_peaceful()
    quality += try_generic_angry()
    #
    if digital:
        return get_digital(quality)
    else:
        return quality
# end def

# sad
@sentiment
def ispeaceful(text: str, digital=True) -> float:
    quality = 0
    # try to match words & context to change the disposition
    quality += try_generic_peaceful()
    quality -= try_generic_angry()
    #
    if digital:
        return get_digital(quality)
    else:
        return quality
# end def

# sad
@sentiment
def isfun(text: str, digital=True) -> float:
    quality = 0
    # try to match words & context to change the disposition
    quality -= try_generic_fun()
    quality += try_generic_bored()
    #
    if digital:
        return get_digital(quality)
    else:
        return quality
# end def

# sad
@sentiment
def isbored(text: str, digital=True) -> float:
    quality = 0
    # try to match words & context to change the disposition
    quality += try_generic_bored()
    quality -= try_generic_fun()
    #
    if digital:
        return get_digital(quality)
    else:
        return quality
# end def

# sad
@sentiment
def issafe(text: str, digital=True) -> float:
    quality = 0
    # try to match words & context to change the disposition
    quality -= try_generic_safety()
    quality += try_generic_fear()
    #
    if digital:
        return get_digital(quality)
    else:
        return quality
# end def

# sad
@sentiment
def isafraid(text: str, digital=True) -> float:
    quality = 0
    # try to match words & context to change the disposition
    quality += try_generic_fear()
    quality -= try_generic_safety()
    #
    if digital:
        return get_digital(quality)
    else:
        return quality
# end def

    #-------------#
    #     try     #
    #-------------#

# try to match words in the dictionary

# happy
def try_generic_happy() -> float:
    temp={}
    for k,v in happy.DATA.items():
        temp[k]=v
    return __try(temp, happy.HASHTAGS)
# end def

# sad
def try_generic_sad() -> float:
    temp={}
    for k,v in sad.DATA.items():
        temp[k]=v
    return __try(temp, sad.HASHTAGS)
# end def
    
# happy
def try_generic_angry() -> float:
    temp={}
    for k,v in angry.DATA.items():
        temp[k]=v
    return __try(temp, angry.HASHTAGS)
# end def

# sad
def try_generic_peaceful() -> float:
    temp={}
    for k,v in peaceful.DATA.items():
        temp[k]=v
    return __try(temp, peaceful.HASHTAGS)
# end def
    
# happy
def try_generic_fun() -> float:
    temp={}
    for k,v in fun.DATA.items():
        temp[k]=v
    return __try(temp, fun.HASHTAGS)
# end def

# sad
def try_generic_bored() -> float:
    temp={}
    for k,v in bored.DATA.items():
        temp[k]=v
    return __try(temp, bored.HASHTAGS)
# end def
    
# happy
def try_generic_safety() -> float:
    temp={}
    for k,v in safe.DATA.items():
        temp[k]=v
    return __try(temp, safe.HASHTAGS)
# end def

# sad
def try_generic_fear() -> float:
    temp={}
    for k,v in fear.DATA.items():
        temp[k]=v
    return __try(temp, fear.HASHTAGS)
# end def
    
def __try(_dict: dict, hashtags: str) -> float:
    '''
        Function to test the sentiment of a string stored in G.text
        by using a dictionary of sentiment-words and a string of
        hashtags, both taken from a sentiment file such as happy.py.
        
        Parameters:
            _dict: dictionary of sentiment-words to try to match
                {word : ranking}
            hashtags: string of hashtags to try to match
        Returns:
            quality: float from -1 to 1
    '''
    # init
    matches = []
    _add_common_misspellings(_dict)
    quality = 0
    nextQuality_a = 0
    nextQuality_m = 1
    lastQuality = 0
    
##    print("first it's ",quality)
    
    # hashtags
    sethashtags = extract_hashtags(hashtags)
    for word in G.hashtags:
        if word in sethashtags:
            mm=1.5
            quality += 0.5 + mm - mm*(hashtags.find(word) / len(hashtags))
            
    
##    print("then it's ",quality)
    #
    # iterate over all nouns
    _tk = tokenizers.WordTokenizer()
    for word in _tk.itokenize(G.text, include_punc=True): # blob.noun_phrases
        # (common word pairs -- words that commonly go together?)
        
        # hashtags
##        if '#'==word:
##            nextQuality_m = 1.5
##            continue
        if '.'==word:
            nextQuality_m = 1
            nextQuality_a = 1
            lastQuality = 0
            continue
        
        
        # grammar context #
        
        # qualifiers
        for k,v in PREFIX_QUALIFIERS.items():
            vm, va = v
            if k == word:
                nextQuality_a += va
                nextQuality_m *= vm
                continue
        for k,v in POSTFIX_QUALIFIERS.items():
            vm, va = v
            if k == word:
                quality *= (va*lastQuality + vm*lastQuality)
                continue
        
        # matches with keywords / phrases
        for k,v in _dict.items():
            # check for a match
            if k == word:
                # check for context (negation?, qualifiers?, etc.)
                    # qualifiers e.g. "very", "slightly" etc.
                lastQuality = nextQuality_m*(nextQuality_a + ranktof(v))
                quality += lastQuality
                matches.append(word)
                nextQuality_a = 0
                nextQuality_m = 1
        # end for
    # end for
    
    # idea: take into account the frequency of selected words
    #   and their ratio to the total number of words?
##    numMatches = len(matches)
    
##    print("final q: ",quality)
    return min(1, quality)
# end def

def _add_common_misspellings(_dict: dict, quality=-1):
    pass #TODO
def _add_common_abbreviations(_dict: dict, quality=-1):
    pass #TODO

def get_training_data_from_text(sentiment: str, *args):
    data=[]
    for arg in args:
        data.append(test(arg, sentiment))

if __name__ == "__main__":
    ''' testing '''
    init()
    _tk = tokenizers.WordTokenizer()
    words = []
    while (True):
        print("Enter the text to test: ")
        text = input()
        blob = TextBlob(text)
        print(test(text, 'happy'))
        
##        print("blob: ",blob)
##        for noun in blob.noun_phrases:
##            print(noun)
##        print("words...")
##        for word in _tk.itokenize(text):
##            words.append(word)
##            print(word.lower())





