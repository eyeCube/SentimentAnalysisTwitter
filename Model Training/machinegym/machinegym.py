
from textblob import TextBlob
from happy import _dict as HAPPY
from sad import _dict as SAD

'''
    import nltk
    nltk.download('brown')
    nltk.download('punkt')
'''

# ranks
# how well does the word match the sentiment?

_S=7
_A=6
_B=5
_C=4
_D=3
_E=2
_F=1

__S = 1
__A = 0.75
__B = 0.5
__C = 0.3333334
__D = 0.25
__E = 0.2
__F = 0.1666667

__RANKTOF={
_F : __F,
_E : __E,
_D : __D,
_C : __C,
_B : __B,
_A : __A,
_S : __S,
    }

def init(): # call this before running any other scripts.
    # negative ranks
    for k,v in __RANKTOF.items():
        k = min(_S, abs(k)) * sign(k)
        __RANKTOF[-k] = -v

def ranktof(i: int) -> float:
    return __RANKTOF.get(math.sqrt(i), 0)
def sign(f: float) -> int:
    if f < 0: return -1
    if f > 0: return 1
    return 0

class G:
    blob=None
    hashtags=None
# end class

def extract_hashtags(text: str) -> set:
    return set(part[1:] for part in text.split(' ') if part.startswith('#'))

def en_check(blob: TextBlob) -> bool:
    return ( blob.detect_language()=='en' )

def test(text: str, _type: str) -> float:
    ''' test the text 'text' for the sentiment given by the string '_type'.
        Returns a float from -1 to 1, which indicates how well it matches
            the given sentiment.
    '''
    if _type=='happy':
        return ishappy(text)
    if _type=='': #TODO: other sentiments
        return ishappy(text)
# end def

    #------------------#
    #    sentiments    #
    #------------------#

# happy
def ishappy(text: str) -> float:
    G.blob = TextBlob(text)
    G.hashtags = extract_hashtags(text)
    quality = 0
    n = 0
    # try to match some sentimental words/phrases/hashtags
    quality += try_generic_happy(); n+=1;
    quality -= try_generic_sad(); n+=1;
    if n!=1: quality /= n
    return quality
# end def

    #-------------#
    #     try     #
    #-------------#

# happy
def try_generic_happy() -> float:
    return __try(SAD)
# end def

# sad
def try_generic_sad() -> float:
    return __try(HAPPY)
# end def
    
def __try(_dict: dict) -> float:
    ''' Returns: (float, int,) | (quality, numMatches,) '''
    # init
    quality = 0
    numMatches = 0
    _improve_quality_of_hashtags(_dict)
    _add_common_misspellings(_dict)
    hashtag = False
    #
    # iterate over all nouns
    for noun in blob.noun_phrases:
        if '#'==noun:
            hashtag = True
            continue
        for k,v in kwargs.items():
            # check for a match
            if k == noun:
                if hashtag:
                    quality += 1
                quality += ranktof(v)
                numMatches += 1
        # end for
        hashtag = False
    # end for
    
    # take into account the frequency of selected words
    # and their ratio to the total number of words
        # TODO
##    numMatches
    
    return min(1, quality)
# end def

def _improve_quality_of_hashtags(_dict: dict, quality=1):
    for word in G.hashtags:
        if word in _dict.keys():
            _dict[word] += quality

def _add_common_misspellings(_dict: dict, quality=-1):
    pass #TODO

if __name__ == "__main__":
    init()
    print("Enter the text to test: ")
    blob = TextBlob(input())
    for noun in blob.noun_phrases:
        print(noun)
##    print(test(input(), 'happy'))
    
