
from textblob import TextBlob, tokenizers
from meta import *
from happy import DATA as HAPPY
from sad import DATA as SAD
from grammar import QUALIFIERS

'''
    import nltk
    nltk.download('brown')
    nltk.download('punkt')
'''

class G: # global data
    text=None
    blob=None
    hashtags=None
# end class

def init(): # call this before running any other scripts.
    # negative ranks
    temp={}
    for k,v in C__RANKTOF.items():
        k = min(C_S, abs(k)) * sign(k)
        temp[-k] = -v
    for k,v in temp.items():
        C__RANKTOF[k] = v

def ranktof(i: int) -> float:
    ii = min(C_S, abs(i)) * sign(i)
    return C__RANKTOF.get(ii, 0) #math.sqrt(i)
def sign(f: float) -> int:
    if f < 0: return -1
    if f > 0: return 1
    return 0

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
    if _type=='sad':
        return issad(text)
    #TODO: other sentiments
# end def

    #------------------#
    #    sentiments    #
    #------------------#

# happy
def ishappy(text: str) -> float:
    G.text = text
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
    quality = lastQuality = 0
    matches = []
    _improve_quality_of_hashtags(_dict)
    _add_common_misspellings(_dict)
    nextQuality = 0
    #
    # iterate over all nouns
    _tk = tokenizers.WordTokenizer()
    for word in _tk.itokenize(G.text, include_punc=True): # blob.noun_phrases
        # TODO: get and compare phrases instead of words (HOW TO?)
        # (common word pairs -- words that commonly go together)
        
        # hashtags
        if '#'==word:
            nextQuality += 1
            continue
        if '.'==word:
            nextQuality = 0
            lastQuality = 0
            continue
        
        
        # grammar context #
        
        # qualifiers
        for k,v in PREFIX_QUALIFIERS.items():
            vm, va = v
            if k == word:
                nextQuality += va
                nextQuality *= vm
                continue
        for k,v in POSTFIX_QUALIFIERS.items():
            vm, va = v
            if k == word:
                quality += va*lastQuality
                quality *= vm*lastQuality
                continue
        
        # matches with keywords / phrases
        for k,v in kwargs.items():
            # check for a match
            if k == word:
                # check for context (negation?, qualifiers?, etc.)
                    # qualifiers e.g. "very", "slightly" etc.
                #   (TODO)
                lastQuality = nextQuality + ranktof(v)
                quality += lastQuality
                matches.append(word)
                nextQuality = 0
        # end for
    # end for
    
    # take into account the frequency of selected words
    # and their ratio to the total number of words
        # TODO
##    numMatches = len(matches)
    
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
    _tk = tokenizers.WordTokenizer()
    words = []
    while (True):
        print("Enter the text to test: ")
        text=input()
        blob = TextBlob(text)
        print("blob: ",blob)
        for noun in blob.noun_phrases:
            print(noun)
        print("words...")
        for word in _tk.itokenize(text):
            words.append(word)
            print(word.lower())
##    print(test(input(), 'happy'))
    
