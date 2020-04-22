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

from textblob import TextBlob, tokenizers

from ModelTraining.machinegym.meta import *
import ModelTraining.machinegym.happy as happy
import ModelTraining.machinegym.sad as sad
import ModelTraining.machinegym.angry as angry
import ModelTraining.machinegym.peaceful as peaceful
from ModelTraining.machinegym.grammar import PREFIX_QUALIFIERS, POSTFIX_QUALIFIERS

class G: # global data
    blob=None
    text=""
    hashtags=set()
# end class

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
    ''' get the quality amount for a given integer rank '''
    ii = min(C_S, abs(i)) * sign(i)
    return C__RANKTOF.get(ii, 0) #math.sqrt(i)
def sign(f: float) -> int: # numerical sign, positive, negative, or 0
    if f < 0: return -1
    if f > 0: return 1
    return 0

def extract_hashtags(text: str) -> set: # get words beginning with '#' (hashtags)
    split=[]
    temp=[]
    for i in text.split('\n'):
        temp.append(i)
    for j in temp:
        for i in j.split(' '):
            split.append(i)
    return set(part[1:] for part in split if part.startswith('#'))

def en_check(blob: TextBlob) -> bool: # is language of text English?
    return ( blob.detect_language()=='en' )

def test(text: str, _type: str, digital=True) -> float:
    ''' test the text 'text' for the sentiment given by the string '_type'.
        Returns a float from -1 to 1, which indicates how well it matches
            the given sentiment.
    '''
    if _type=='happy':
        return ishappy(text, digital=digital)
    if _type=='sad':
        return issad(text, digital=digital)
    if _type=='angry':
        return isangry(text, digital=digital)
    if _type=='peaceful':
        return ispeaceful(text, digital=digital)
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
def sentiment(func): # wrapper function to initialize an is_sentiment function
    def inner(*args, **kwargs):
        text = args[0]
        G.text = text
        G.blob = TextBlob(text)
        G.hashtags = extract_hashtags(text)
        return func(*args, **kwargs)
    return inner

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
    
def __try(_dict: dict, hashtags: str) -> float: # returns quality: float from -1 to 1
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
        # TODO: get and compare phrases instead of words (HOW TO?)
        # (common word pairs -- words that commonly go together)
        
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
                #   (TODO)
                lastQuality = nextQuality_m*(nextQuality_a + ranktof(v))
                quality += lastQuality
                matches.append(word)
                nextQuality_a = 0
                nextQuality_m = 1
        # end for
    # end for
    
    # take into account the frequency of selected words
    # and their ratio to the total number of words
        # TODO
##    numMatches = len(matches)
    
##    print("final q: ",quality)
    return min(1, quality)
# end def

def _add_common_misspellings(_dict: dict, quality=-1):
    pass #TODO
def _add_common_abbreviations(_dict: dict, quality=-1):
    pass #TODO

if __name__ == "__main__":
    init()
    _tk = tokenizers.WordTokenizer()
    words = []
    while (True):
        print("Enter the text to test: ")
        text = input()
        blob = TextBlob(text)
        print(test(text, 'angry'))
        
##        print("blob: ",blob)
##        for noun in blob.noun_phrases:
##            print(noun)
##        print("words...")
##        for word in _tk.itokenize(text):
##            words.append(word)
##            print(word.lower())





